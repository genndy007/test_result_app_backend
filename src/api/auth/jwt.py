import datetime
import jwt

from src.config import Config


def generate_jwt_token(user):
    now = datetime.datetime.now()
    payload = {
        'id': user.id,
        'exp': now + datetime.timedelta(minutes=60),
        'iat': now,
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token
