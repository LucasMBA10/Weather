from .userModel import UserEntity
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .userRepository import UserRepository

def authenticate(username, password):
    user_repo = UserRepository('users')
    filter = {'username': username, 'password': password}
    user_data = user_repo.get(filter)
    
    if user_data:
        user_info = user_data[0]  # Supondo que username seja único
        return UserEntity(username=user_info['username'], 
                          name=user_info.get('name'), 
                          id=user_info.get('id'), 
                          email=user_info.get('email'), 
                          password=user_info['password'])
    return None

def generateToken(user):
    payload = {
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    return jwt.encode(payload=payload, 
                      key=getattr(settings, 'SECRET_KEY'),
                      algorithm='HS256')

def refreshToken(user):
    return generateToken(user)

def verifyToken(token):
    error_code = 0
    payload = None

    try:
        payload = jwt.decode(jwt=token, 
                             key=getattr(settings, 'SECRET_KEY'),
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
