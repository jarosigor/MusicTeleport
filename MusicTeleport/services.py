from datetime import datetime, timedelta
from .models import Token, Playlist
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def save_access_token(user, access_token, refresh_token, expires_in):
    expires_at = datetime.now() + timedelta(seconds=expires_in)
    aware_expires_at = timezone.make_aware(expires_at)

    token = Token(
        user=user,
        token_type='access',
        access_token=access_token,
        expires_at=aware_expires_at,
        refresh_token=refresh_token
    )
    token.save()
    logger.debug('Saved access token')


def save_playlist(user, playlist_details):
    playlist = Playlist(
        user=user,
        name=playlist_details['name'],
        spotify_id=playlist_details['id']
    )
    playlist.save()
