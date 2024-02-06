document.addEventListener('DOMContentLoaded', function() {
    const roomName = JSON.parse(document.getElementById('room_name').textContent.replace(/\s/g, '_'));
    const userName = JSON.parse(document.getElementById('username').textContent.replace(/\s/g, '_'));
    const messageContainer = document.getElementById('message-container');

    const chatSocket = new ReconnectingWebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        appendMessage(data.message.author ,data.message.content);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'from': userName,
                'command':'new_message'
            }));
            messageInputDom.value = '';
        }
    };

    document.querySelector('#create-group-submit').onclick = function(e) {
        window.location.pathname = '/chat/'
    };

    function appendMessage(username,message) {

        const usernameDiv = document.createElement('div');
        usernameDiv.className = 'username';
        usernameDiv.textContent = userName;
        messageContainer.appendChild(usernameDiv);

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.textContent = username + ": " + message;
        messageContainer.appendChild(messageDiv);



        // Scroll to the bottom of the container after appending a new message
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
});
