import spotipy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from spotipy.oauth2 import SpotifyOAuth
from os import getenv
from .forms import PlaylistSelectForm
from .services import save_access_token, save_playlist
import logging


logger = logging.getLogger(__name__)


@login_required
def base(request):
    logger.debug('---Base view---')
    return render(request, "base.html")


@login_required
def home(request):
    logger.debug('---Home view---')
    return render(request, "home.html")


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            logger.info('User registration successful')
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            logger.warning('User registration unsuccessful')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def spotify_authorize(request):
    sp_oauth = SpotifyOAuth(
        client_id=getenv('CLIENT_ID'),
        client_secret=getenv('CLIENT_SECRET'),
        redirect_uri='http://localhost:8000/spotify/callback/',
        scope='user-library-read playlist-read-private'
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@login_required
def spotify_authorize_callback(request):
    logger.debug('Authorizing user...')
    sp_oauth = SpotifyOAuth(
        client_id=getenv('CLIENT_ID'),
        client_secret=getenv('CLIENT_SECRET'),
        redirect_uri='http://localhost:8000/spotify/callback/',
        scope='user-library-read playlist-read-private'
    )
    token_info = sp_oauth.get_access_token(request.GET.get('code'))
    if 'access_token' in token_info:
        logger.debug('callback' + token_info['access_token'])
        save_access_token(request.user, token_info['access_token'], token_info['refresh_token'],
                          token_info['expires_in'])
        return redirect('http://localhost:8000/home/')
    else:
        logger.warning('Failed to receive token')
        return HttpResponse('Authorization failed')


@login_required
def select_playlist(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=getenv('CLIENT_ID'), client_secret=getenv('CLIENT_SECRET'),
                                                   redirect_uri='http://localhost:8000/home/',
                                                   scope='playlist-read-private'))
    playlists_data = sp.current_user_playlists()
    playlists = ((item['id'], item['name']) for item in playlists_data['items'])

    if request.method == 'POST':
        form = PlaylistSelectForm(playlists, request.POST)
        if form.is_valid():
            selected_playlist_id = form.cleaned_data['selected_playlist']
            playlist_items = sp.playlist_items(playlist_id=selected_playlist_id)['items']
            playlist_track_objects = [item['track'] for item in playlist_items]
            track_list = [track['name'] for track in playlist_track_objects]
            print(track_list)
            return render(request, 'playlist_detail.html', {'tracks': track_list})
        else:
            logger.warning('Form not valid')
    else:
        form = PlaylistSelectForm(playlist_choices=playlists)

    logger.debug(playlists)
    return render(request, 'home.html', {'form': form})


@login_required
def spotify_import_playlist(request, playlist_id):
    sp = spotipy.Spotify(auth=SpotifyOAuth)
    playlist_details = sp.playlist(playlist_id)
    save_playlist(request.user, playlist_details)
    return redirect('playlist_list')
