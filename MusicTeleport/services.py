from datetime import datetime, timedelta
from .models import Token
from django.utils import timezone


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
    print('saving token')
    token.save()
