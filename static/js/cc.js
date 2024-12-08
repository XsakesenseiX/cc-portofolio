document.addEventListener('DOMContentLoaded', () => {
    const profiles = document.querySelectorAll('.profile-link');
    
    profiles.forEach(profile => {
        profile.addEventListener('click', (e) => {
            e.preventDefault();
            const username = profile.closest('.profile').getAttribute('data-username');
            const userId = profile.closest('.profile').getAttribute('data-user-id');
            
            // Store user info in localStorage
            localStorage.setItem('selectedUsername', username);
            localStorage.setItem('selectedUserId', userId);
            
            // Redirect to PIN entry page
            window.location.href = '/pin-entry';
        });
    });
});





//---------dash.html---------
/*===== scroll sections active =====*/
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

/*===== chat ai =====*/
document.addEventListener('DOMContentLoaded', () => {
  const chatbotIcon = document.getElementById('chatbot-icon');
  const chatbotContainer = document.getElementById('chatbot-container');
  const closeChatbotBtn = document.getElementById('close-chatbot');
  const chatInput = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  const chatMessages = document.getElementById('chat-messages');

  // Toggle chatbot visibility
  chatbotIcon.addEventListener('click', () => {
      chatbotContainer.style.display = 'flex';
      chatbotIcon.style.display = 'none';
  });

  // Close chatbot
  closeChatbotBtn.addEventListener('click', () => {
      chatbotContainer.style.display = 'none';
      chatbotIcon.style.display = 'flex';
  });

  // Function to add a message to the chat
  function addMessage(message, sender) {
      const messageElement = document.createElement('div');
      messageElement.classList.add('message', sender);
      messageElement.textContent = message;
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Send message to AI
  function sendMessage() {
      const message = chatInput.value.trim();
      if (!message) return;

      // Add user message to chat
      addMessage(message, 'user-message');
      
      // Clear input
      chatInput.value = '';

      // Send to backend
      fetch('/get_ai_response', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: message })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              addMessage(data.response, 'ai-message');
          } else {
              addMessage('Sorry, something went wrong.', 'ai-message');
          }
      })
      .catch(error => {
          console.error('Error:', error);
          addMessage('Sorry, something went wrong.', 'ai-message');
      });
  }

  // Event listeners
  sendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
          sendMessage();
      }
  });
});

/*===== scroll sections active =====*/
let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');

window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            })
        }
    });

/*===== sticky navbar =====*/
let header = document.querySelector('.header');

header.classList.toggle('sticky', window.scrollY > 100);

/*===== remove menu icon navbar =====*/
menuIcon.classList.remove('bx-x');
navbar.classList.remove('active');

};


/*===== sticky navbar =====*/
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 50,
    loop: true,
    grabCursor: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });


  /*===== dark light mode =====*/
  let darkModeIcon = document.querySelector('#darkMode-icon');

  darkModeIcon.onclick = () => {
    darkModeIcon.classList.toggle('bx-sun');
    document.body.classList.toggle('dark-mode');
  };


  /*===== scroll reveal =====*/
  ScrollReveal({
    /*reset: true,*/
    distance: '80px',
    duration: 2000,
    delay: 200
  });


  // Menampilkan preview gambar di pop-up
function showPreview(event) {
  const file = event.target.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
          // Tampilkan pratinjau gambar
          const previewImage = document.getElementById('previewImage');
          previewImage.src = e.target.result;
          previewImage.alt = file.name;

          // Tampilkan nama file
          const fileName = document.getElementById('fileName');
          fileName.textContent = file.name;

          // Tampilkan pop-up
          document.getElementById('popup').style.display = 'flex';
      };
      reader.readAsDataURL(file);
  }
}

// Tutup pop-up tanpa mengunggah file
function closePopup() {
  document.getElementById('popup').style.display = 'none';
}

// Kirim formulir setelah konfirmasi
function confirmUpload() {
  document.getElementById('uploadForm').submit();
}

  ScrollReveal().reveal('.home-content, .heading', {origin: 'top'});
  ScrollReveal().reveal('.home-img img, .portofolio-box, .team-wrapper, contact form', {origin: 'bottom'});
  ScrollReveal().reveal('.home-content h1, .about-img img', {origin: 'left'});
  ScrollReveal().reveal('.home-content h3, .home-content p, .about-content', {origin: 'right'});