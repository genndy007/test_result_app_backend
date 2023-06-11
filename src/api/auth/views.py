import datetime

from flask import request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

from src.models import DBSession, engine
from src.models.user import User, Project
from src.utils import message_response
from . import auth
from .jwt import generate_jwt_token, authenticate_jwt


@auth.route('/db', methods=['GET'])
def db():
    now = datetime.datetime.now()
    with engine.connect() as conn:
        results = conn.execute(text('select version()'))
        version = ''.join([str(row[0]) for row in results])
    return message_response(f'Timestamp: {now}; version: {version}', 200)


@auth.route('/signup', methods=['POST'])
def signup():
    body = request.json

    first_name = body.get('first_name', 'Default')
    last_name = body.get('last_name', 'Default')
    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return message_response('Fields `username`, `password` are required!', 400)

    existing_user = DBSession.query(User).filter(User.username == username).first()
    if existing_user:
        return message_response('User already exists!', 202)

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        active_project_id=None,
    )
    DBSession.add(user)
    DBSession.commit()

    project = Project(
        user_id=user.id,
        name='Default project',
        description='Default description'
    )
    DBSession.add(project)
    DBSession.commit()

    user.active_project_id = project.id
    DBSession.commit()
    return message_response('Successfully registered!', 201)


@auth.route('/login', methods=['POST'])
def login():
    body = request.json

    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return message_response('Fields `username`, `password` are required!', 400)

    user = DBSession.query(User).filter(User.username == username).first()
    if not user:
        return message_response(f'Username `{username}` does not exist', 401)

    if check_password_hash(user.password_hash, password):
        token = generate_jwt_token(user)
        welcome_message = f'Welcome, {user.full_name}! Authenticated with username `{username}`'
        response = message_response(welcome_message, 200)
        response.set_cookie('jwt', token)
        return response
    return message_response(f'Wrong password', 401)


@auth.route('/me', methods=['GET'])
def me():
    payload = authenticate_jwt(request)
    if not payload:
        return message_response('Authenticate at /auth/login first', 403)

    user_id = payload['id']
    user = DBSession.query(User).filter(User.id == user_id).first()
    project = DBSession.query(Project).filter(Project.id == user.active_project_id).first()
    user_info = {
        'id': user_id,
        'full_name': user.full_name,
        'username': user.username,
        'active_project': {
            'name': project.name,
            'description': project.description,
        }
    }

    return make_response({'user': user_info}, 200)
