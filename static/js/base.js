document.addEventListener('DOMContentLoaded', function() {
    const authorizeButton = document.getElementById('authorizeButton');
    const logoutButton = document.getElementById('logoutButton');

    authorizeButton.addEventListener('click', function() {
        window.location.href = 'http://localhost:8000/spotify/authorize/';
    });

    logoutButton.addEventListener('click', function () {
        window.location.href = 'http://localhost:8000/logout/';
    })

});
