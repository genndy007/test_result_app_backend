from flask import request, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from src.models import DBSession
from src.models.user import User, Project


@auth.route('/ping', methods=['GET'])
def ping():
    return make_response({'message': 'Pong!'}, 200)


@auth.route('/signup', methods=['POST'])
def signup():
    body = request.json

    first_name = body.get('first_name', 'Default')
    last_name = body.get('last_name', 'Default')
    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return make_response({'message': 'Fields `username`, `password` are required!'}, 400)

    existing_user = DBSession.query(User).filter(User.username == username).first()
    if not existing_user:
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
        return make_response({'message': 'Successfully registered!'}, 201)
    else:
        return make_response({'message': 'User already exists!'}, 202)

