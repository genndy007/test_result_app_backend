import datetime
import jwt

from src.config import Config


def generate_jwt_token(user):
    now = datetime.datetime.utcnow()
    payload = {
        'id': user.id,
        'exp': now + datetime.timedelta(minutes=60),
        'iat': now,
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def authenticate_jwt(request):
    token = request.cookies.get('jwt')
    if not token:
        return

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except Exception as e:
        print(e)
        return
