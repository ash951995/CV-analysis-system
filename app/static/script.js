document.addEventListener('DOMContentLoaded', function() { // Run after DOM loads.
    const sendButton = document.getElementById('sendButton'); // Change the id to match your html
    const queryInput = document.getElementById('queryInput');
    const messagesDiv = document.getElementById('messages');

    if (sendButton && queryInput && messagesDiv) {
        sendButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission if needed

            const query = queryInput.value;

            fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => response.json())
            .then(data => {
                messagesDiv.innerHTML += `<p>User: ${query}</p><p>Bot: ${data.response}</p>`;
                queryInput.value = '';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    } else {
        console.error("One or more elements not found.");
    }
});