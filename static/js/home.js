document.addEventListener('DOMContentLoaded', function() {
    const authorizeButton = document.getElementById('importPlaylistButton');
    const logoutButton = document.getElementById('logoutButton');

    authorizeButton.addEventListener('click', function() {
        window.location.href = 'home/import-playlist/';
    });

    logoutButton.addEventListener('click', function () {
        window.location.href = 'logout/';
    })

});