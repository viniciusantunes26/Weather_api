import jwt
from datetime import datetime, timedelta
from django.conf import settings

from .models import UserEntity

def authenticate(username, password):
    if username == 'user' and password == 'a1b2c3':
        user = UserEntity(username=username, password=password)
        print(user)
        return user
    return None

def generateToken(user):
    payload = {
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(payload=payload,
                      key=getattr(settings, "SECRET_KEY"),
                      algorithm='HS256')

def refreshToken(user):
    return generateToken(user)

def verifyToken(token):
    error_code = 0
    payload = None
    try:
        payload = jwt.decode(jwt=token,
                      key=getattr(settings, "SECRET_KEY"),
                      algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2

    return [error_code, payload]

def getAuthenticatedUser(token):
    _, payload = verifyToken(token)

    if payload is not None:
        return UserEntity(username=payload['username'])