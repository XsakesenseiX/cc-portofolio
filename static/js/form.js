//---------form.html----------
document.addEventListener('DOMContentLoaded', () => {
    const username = localStorage.getItem('selectedUsername');
    const userId = localStorage.getItem('selectedUserId');
    const usernameDisplay = document.getElementById('username-display');
    const pinInput = document.getElementById('pin-input');
    const submitButton = document.getElementById('submit-pin');
    const errorMessage = document.getElementById('error-message'); // Add this element to your HTML
    const dots = document.querySelectorAll('.dot');

    // Validate that user is selected
    if (!username || !userId) {
        alert('Please select a user first');
        window.location.href = '/pin-entry';
        return;
    }

    // Display username
    usernameDisplay.textContent = `Welcome, ${username}`;

    // Reset error message
    function resetError() {
        if (errorMessage) {
            errorMessage.textContent = '';
            errorMessage.style.display = 'none';
        }
    }

    // Show error message
    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        } else {
            alert(message);
        }
    }

    // Pin input dots animation
    pinInput.addEventListener('input', () => {
        resetError(); // Clear any previous error
        const pinLength = pinInput.value.length;
        dots.forEach((dot, index) => {
            if (index < pinLength) {
                dot.classList.add('filled');
            } else {
                dot.classList.remove('filled');
            }
        });

        // Automatically submit if 4 digits are entered
        if (pinLength === 4) {
            submitPin();
        }
    });

    submitButton.addEventListener('click', submitPin);

    function submitPin() {
        const pin = pinInput.value;
        const userId = localStorage.getItem('selectedUserId');
    
        // More robust error handling
        if (!userId) {
            showError('No user selected. Please go back and select a user.');
            return;
        }
    
        if (pin.length !== 4 || !/^\d+$/.test(pin)) {
            showError('Please enter a 4-digit PIN');
            return;
        }
    
        fetch('/verify-pin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userId: userId,
                pin: pin
            })
        })
        .then(response => {
            // Log response for debugging
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            
            if (data.success) {
                // Store both username and full name in localStorage
                localStorage.setItem('selectedUsername', data.username);
                localStorage.setItem('selectedFullName', data.full_name);
                window.location.href = data.redirectUrl;
            } else {
                showError(data.error || 'Login failed');
                pinInput.value = '';
                dots.forEach(dot => dot.classList.remove('filled'));
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            showError('Network error. Please try again.');
        });
    }

    // Optional: Add keyboard support
    pinInput.addEventListener('keydown', (e) => {
        // Allow only numbers and backspace
        if (!/^[0-9]$/.test(e.key) && e.key !== 'Backspace') {
            e.preventDefault();
        }
    });
});