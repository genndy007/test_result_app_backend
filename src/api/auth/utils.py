from src.models import DBSession
from src.models.user import User
from src.security.jwt import authenticate_jwt


def get_current_user(request):
    payload = authenticate_jwt(request)
    if not payload:
        return

    user_id = payload['id']
    user = DBSession.query(User).filter(User.id == user_id).first()
    return user
