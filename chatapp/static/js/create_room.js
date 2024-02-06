document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

    document.querySelector('#room-name-input').focus();

    document.querySelector('#room-name-input').onkeyup = function(e) {
        if (e.key === 'Enter') {
            document.querySelector('#room-password-input').focus();
        }
    };

    document.querySelector('#room-password-input').onkeyup = function(e) {
        if (e.key === 'Enter') {
            document.querySelector('#room-create-submit').click();
        }
    };

    document.querySelector('#room-create-submit').onclick = function(e) {
        var roomName = document.querySelector('#room-name-input').value;
        var roomPassword = document.querySelector('#room-password-input').value;

        const data = {
            'roomName': roomName,
            'roomPassword': roomPassword,
        };

        const { protocol, host, pathname } = window.location;

        const endpointUrl = `${protocol}//${host}${pathname}`;


        fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data), 
        })
        .then(response => {
            if (response.redirected) {
                
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    };
});