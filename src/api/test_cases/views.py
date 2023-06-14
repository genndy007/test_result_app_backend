from http import HTTPStatus

from flask import request, make_response
from sqlalchemy.orm import selectinload

from src.api.auth.utils import get_current_user
from src.models import DBSession
from src.models.test_case import TestCase, TestStep
from src.utils import message_response
from .validate import validate_test_steps
from . import test_cases


@test_cases.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    active_project_test_cases = DBSession.query(TestCase)\
        .filter(TestCase.project_id == user.active_project_id)\
        .options(selectinload(TestCase.test_steps))\
        .order_by(TestCase.id.desc())\
        .all()

    test_cases_list = []
    for test_case in active_project_test_cases:
        test_case_item = {
            'id': test_case.id,
            'name': test_case.name,
            'description': test_case.description,
            'precondition': test_case.precondition,
            'postcondition': test_case.postcondition,
            'test_steps': [
                {
                    'content': test_step.content,
                    'order': test_step.order,
                } for test_step in test_case.test_steps
            ],
        }
        test_cases_list.append(test_case_item)

    return make_response({'test_cases': test_cases_list}, HTTPStatus.OK)


@test_cases.route('/new', methods=['POST'])
def new():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    name = request.json.get('name')
    description = request.json.get('description')
    precondition = request.json.get('precondition')
    postcondition = request.json.get('postcondition')
    test_steps = request.json.get('test_steps')

    if not all([name, description, precondition, postcondition, test_steps]):
        msg = 'Required fields: name,description,precondition,postcondition,test_steps'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    if not validate_test_steps(test_steps):
        return message_response('Each test_step must contain content,order', HTTPStatus.BAD_REQUEST)

    test_case = TestCase(
        project_id=user.active_project_id,
        name=str(name),
        description=str(description),
        precondition=str(precondition),
        postcondition=str(postcondition)
    )
    DBSession.add(test_case)
    DBSession.commit()

    for test_step in test_steps:
        new_test_step = TestStep(
            test_case_id=test_case.id,
            content=str(test_step['content']),
            order=int(test_step['order']),
        )
        DBSession.add(new_test_step)
    DBSession.commit()

    return message_response(f'Successfully added new TestCase with id {test_case.id}', HTTPStatus.CREATED)


# todo: no validation if test case exists
@test_cases.route('/delete', methods=['DELETE'])
def delete_by_id():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_case_id = request.args.get('id')
    if not test_case_id:
        return message_response('Required query param `id`', HTTPStatus.BAD_REQUEST)

    DBSession.query(TestCase)\
        .filter(TestCase.project_id == user.active_project_id)\
        .filter(TestCase.id == test_case_id)\
        .delete()
    DBSession.commit()

    return message_response(f'Successfully deleted TestCase with id {test_case_id}', HTTPStatus.NO_CONTENT)
