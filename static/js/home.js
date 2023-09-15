document.addEventListener('DOMContentLoaded', function() {
    const importPlaylistButton = document.getElementById('importPlaylistButton');
    const logoutButton = document.getElementById('logoutButton');
    const submitPlaylistButton = document.getElementById('submitPlaylistButton');

    importPlaylistButton.addEventListener('click', function() {
        window.location.href = 'http://localhost:8000/home/import-playlist/';
    });

    logoutButton.addEventListener('click', function () {
        window.location.href = 'http://localhost:8000/logout/';
    });

    submitPlaylistButton.addEventListener('click', function () {
        window.location.href = 'http://localhost:8000/home/import-playlist/list-songs/';
    });

});