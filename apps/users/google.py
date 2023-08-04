from . import serializers
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.exceptions import AuthenticationFailed
from base.base_auth import create_token
from .models import User
from django.conf import settings

def check_google_auth(google_user: serializers.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
         return AuthenticationFailed(code=403, detail='bad token Google')
    

    user, _ = User.objects.get_or_create(email=google_user['email'])
    return create_token(user.id)