document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

    const roomNameInput = document.querySelector('#room-name-input');
    const roomPasswordInput = document.querySelector('#room-password-input');
    const submitButton = document.querySelector('#submit');

    roomNameInput.focus();

    roomNameInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            roomPasswordInput.focus();
        }
    });

    roomPasswordInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            submitButton.click();
        }
    });

    submitButton.addEventListener('click', function() {
        const roomName = roomNameInput.value;
        const roomPassword = roomPasswordInput.value;

        const data = {
            'roomName': roomName,
            'roomPassword': roomPassword,
        };

        const endpointUrl = window.location.href;

        fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(errorData => {
                    console.error('Error:', errorData.error);

                    
                    if (errorData.error) {
                        
                        if (errorData.error.roomName) {
                            alert(errorData.error.roomName);
                        }
                        if (errorData.error.roomPassword) {
                            alert(errorData.error.roomPassword);
                        }
                    } else {
                    
                        alert('An error occurred. Please try again.');
                    }

                    throw new Error('Request failed');
                });
            }
        })
        .then(data => {
            console.log('Success:', data);
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
