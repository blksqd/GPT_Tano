$(document).ready(function () {
    $('#input-form').on('submit', function (e) {
      e.preventDefault();
      let user_input = $('#user_input').val();
      $('#messages').append('<p class="user-message">' + user_input + '</p>');
      $('#user_input').val('');

      // Show the loading dots when waiting for the chatbot's response
      toggleLoadingDots();

      $.ajax({
        type: 'POST',
        url: '/ask',
        data: {user_input: user_input},
        success: function (data) {
          // Hide the loading dots before showing the chatbot's response
          toggleLoadingDots();

          let response = data.response;
          $('#messages').append('<p class="bot-message">' + response + '</p>');
          scrollToBottom(); // Updated line for scrolling to the bottom
        }
      });
    });
});

// Function to scroll to the bottom of the chatbox
function scrollToBottom() {
  const chatbox = document.getElementById('chatbox');
  chatbox.scrollTop = chatbox.scrollHeight;
}

function toggleLoadingDots() {
    const loadingDots = document.querySelector('.loading-dots');
    if (loadingDots.style.display === 'none') {
      loadingDots.style.display = 'inline-block';
    } else {
      loadingDots.style.display = 'none';
    }
}

// Get the initial message element
const initialMessage = document.getElementById('initial-message');

// Remove the initial message element after the first message is sent
document.querySelector('form').addEventListener('submit', function() {
  initialMessage.remove();
});