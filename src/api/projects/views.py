from http import HTTPStatus

from flask import request, make_response

from src.api.auth.utils import get_current_user
from src.models import DBSession
from src.models.user import Project
from src.utils import message_response
from . import projects


@projects.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    projects_list = []
    projects_qs = DBSession.query(Project).filter(Project.user_id == user.id)
    for project in projects_qs:
        is_active = project.id == user.active_project_id
        project_dict = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'is_active': is_active,
        }
        projects_list.append(project_dict)

    return make_response({'projects': projects_list}, HTTPStatus.OK)


@projects.route('/new', methods=['POST'])
def new():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    name = request.json.get('name')
    description = request.json.get('description')

    if not all([name, description]):
        msg = 'Required fields: name,description'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    project = Project(
        user_id=user.id,
        name=name,
        description=description,
    )
    DBSession.add(project)
    DBSession.commit()

    return message_response(f'Successfully created project with id `{project.id}`', HTTPStatus.CREATED)


@projects.route('/set_active', methods=['PUT'])
def set_active():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    project_id = request.args.get('id')
    if not project_id:
        return message_response('Required query param `id`', HTTPStatus.BAD_REQUEST)

    existing_project = DBSession.query(Project)\
        .filter(Project.user_id == user.id)\
        .filter(Project.id == project_id).first()
    if not existing_project:
        return message_response(f'Cannot find project with id `{project_id}`', HTTPStatus.NOT_FOUND)

    user.active_project_id = project_id
    DBSession.commit()

    return message_response(f'Successfully set active project with id `{project_id}` to user `{user.full_name}`', HTTPStatus.ACCEPTED)




