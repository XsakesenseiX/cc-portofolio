from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
import mysql
import mysql.connector
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename
import google.generativeai as genai


db_config = {
    'host': ('maltekk.mysql.database.azure.com'),
    'user': ('adminadminadmin'),
    'password': ('Admin12345'),
    'database': ('maltekk-db')
}

def get_azure_db_connection():
    try:
        connection = mysql.connector.connect(
            #user="adminadminadmin", password="Admin12345", host="maltekk.mysql.database.azure.com", port=3306, database="maltekk-db"
            cnx = mysql.connector.connect(user="adminadminadmin", password="Admin12345", host="maltekk.mysql.database.azure.com", port=3306, database="maltekk-db")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def test_database_connection():
    try:
        connection = get_azure_db_connection()
        if connection.is_connected():
            print("Successfully connected to the database!")
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"Database Version: {db_version[0]}")
            cursor.close()
            connection.close()
        else:
            print("Connection failed.")
    except Exception as e:
        print(f"Connection test failed: {e}")

# Call this function to verify connection
test_database_connection()

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
genai.configure(api_key='AIzaSyD1kcYbZQfSGkneurkI5lfaqpd54dFyd54')




@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    try:
        # Get the user's message from the request
        data = request.json
        user_message = data.get('message', '')

        # Configure the model
        model = genai.GenerativeModel('gemini-pro')

        # Generate response
        response = model.generate_content(user_message)

        # Return the AI's response
        return jsonify({
            'success': True,
            'response': response.text
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# PIN Verification Route
@app.route('/verify-pin', methods=['POST'])
def verify_pin():
    data = request.json
    user_id = data.get('userId')
    pin = data.get('pin')

    conn = get_azure_db_connection()
    if not conn:
        return jsonify({
            'success': False, 
            'error': 'Database connection failed'
        }), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Ensure you select full_name from the users table
        query = "SELECT userId, username, full_name FROM users WHERE userId = %s AND pin = %s"
        cursor.execute(query, (user_id, pin))
        user = cursor.fetchone()
        
        if user:
            # Store full_name in the session if needed
            session['full_name'] = user['full_name']
            return jsonify({
                'success': True, 
                'username': user['username'],
                'full_name': user['full_name'],  # Send full name to client
                'userId': user['userId'],
                'redirectUrl': '/dashboard'
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Invalid credentials'
            }), 401

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({
            'success': False, 
            'error': 'Database error occurred',
            'details': str(err)
        }), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

# Routes for page rendering
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/pin-entry/')
def pin_entry():
    return render_template('form.html')

@app.route('/dashboard/')
def dashboard():
    # Retrieve full name from session
    full_name = session.get('full_name', 'User')
    
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT gambar FROM image')
        images = cursor.fetchall()
        return render_template('dash.html', images=images, full_name=full_name)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500
    finally:
        if conn:
            cursor.close()
            conn.close()


# Konfigurasi folder untuk menyimpan file unggahan
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('dashboard'))
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('dashboard'))
        
        # If file is valid, save it
        if file:
            # Generate a unique filename to prevent overwriting
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Insert filename into database
            cursor = conn.cursor()
            cursor.execute('INSERT INTO image (gambar) VALUES (%s)', (filename,))
            conn.commit()
            
            flash('File uploaded successfully')
            return redirect(url_for('dashboard'))
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash(f'Database error: {err}')
        return redirect(url_for('dashboard'))
    
    finally:
        if conn:
            conn.close()
    

@app.route('/kegiatan/')
def kegiatan():
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ak")
        result = cursor.fetchall()
        return render_template('kegiatan.html', ak=result)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/tambah_kegiatan/', methods = ['POST'])
def tambah_kegiatan():
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        flash("Data Inserted Successfully")
        nama = request.form['nama']
        hari = request.form['hari']
        tanggal = request.form['tanggal']
        kegiatan = request.form['kegiatan']
        keterangan = request.form['keterangan']
        
        cursor = conn.cursor()
        cursor.execute ('INSERT INTO ak (nama, hari, tanggal, kegiatan, keterangan) VALUES (%s, %s, %s, %s, %s)', 
        (nama, hari, tanggal, kegiatan, keterangan))
        conn.commit()
        
        return redirect(url_for('kegiatan'))
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash(f'Database error: {err}')
        return redirect(url_for('kegiatan'))
    
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/update_kegiatan/', methods= ['GET','POST'])
def update_kegiatan():
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        nama = request.form['nama']
        hari = request.form['hari']
        tanggal = request.form['tanggal']
        kegiatan = request.form['kegiatan']
        keterangan = request.form['keterangan']
        
        cursor = conn.cursor()
        sql = '''UPDATE ak
        SET hari=%s, tanggal=%s, kegiatan=%s, keterangan=%s
        where nama=%s '''
        value = (hari, tanggal, kegiatan, keterangan, nama)
        cursor.execute(sql, value)
        conn.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('kegiatan'))
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500
    
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route('/hapus_kegiatan/<nama>', methods = ['GET'])
def hapus_kegiatan(nama):
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        flash("Record Has Been Deleted Successfully")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ak WHERE nama=%s", (nama,))
        conn.commit()
        return redirect(url_for('kegiatan'))
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500
    
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
