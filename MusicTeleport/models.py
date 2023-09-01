from django.db import models
from django.utils import timezone


class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token_type = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'MusicTeleport'


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=50, unique=True)
