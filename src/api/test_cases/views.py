from http import HTTPStatus

from flask import request, make_response
from sqlalchemy.orm import selectinload

from src.models import DBSession
from src.models.user import User
from src.models.test_case import TestCase
from src.security.jwt import authenticate_jwt
from src.utils import message_response
from . import test_cases


@test_cases.route('/list_my', methods=['GET'])
def list_my():
    payload = authenticate_jwt(request)
    if not payload:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    user_id = payload['id']
    user = DBSession.query(User).filter(User.id == user_id).first()

    active_project_test_cases = DBSession.query(TestCase)\
        .filter(TestCase.project_id == user.active_project_id)\
        .options(selectinload(TestCase.test_steps))\
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
