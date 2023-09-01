import spotipy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from spotipy.oauth2 import SpotifyOAuth
from os import getenv

from .models import Playlist
from .services import save_access_token
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
        scope='user-library-read'
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
        scope='user-library-read'
    )
    token_info = sp_oauth.get_access_token(request.GET.get('code'))
    if 'access_token' in token_info:
        print('callback' + token_info['access_token'])
        save_access_token(request.user, token_info['access_token'], token_info['refresh_token'],
                          token_info['expires_in'])
        return redirect('home')
    else:
        logger.warning('Failed to receive  token')
        return HttpResponse('Authorization failed')


@login_required
def list_playlist(request):
    sp = spotipy.Spotify(auth=spotipy.oauth2.SpotifyClientCredentials.get_access_token())
    playlists = sp.current_user_playlists()
    return render(request, '', {'playlists': playlists})


@login_required
def spotify_import_playlist(request, spotify_id):
    sp = spotipy.Spotify(auth=spotipy.oauth2.SpotifyClientCredentials.get_access_token())
    playlist_details = sp.playlist(spotify_id)
    playlist = Playlist(name=playlist_details['name'], spotify_id=playlist_details['id'])
    playlist.save()
    return redirect('playlist_list')
