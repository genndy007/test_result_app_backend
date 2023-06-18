from http import HTTPStatus

from flask import request, make_response

from src.api.auth.utils import get_current_user
from src.models import DBSession
from src.models.test_case import TestCase
from src.models.test_suite import TestSuite, TestCaseTestSuite
from src.utils import message_response
from . import test_suites


@test_suites.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_suites_list = []
    test_suites_qs = DBSession.query(TestSuite)\
        .filter(TestSuite.project_id == user.active_project_id)\
        .order_by(TestSuite.id.desc())
    for test_suite in test_suites_qs:
        test_suite_dict = {
            'id': test_suite.id,
            'name': test_suite.name,
            'description': test_suite.description,
            'test_cases': [],
        }
        test_cases_qs = DBSession.query(TestCase)\
            .join(TestCaseTestSuite, TestCaseTestSuite.test_case_id == TestCase.id)\
            .join(TestSuite, TestSuite.id == TestCaseTestSuite.test_suite_id)\
            .filter(TestSuite.id == test_suite.id)\
            .order_by(TestCaseTestSuite.order)
        for test_case in test_cases_qs:
            test_case_dict = {
                'id': test_case.id,
                'name': test_case.name,
                'description': test_case.description,
            }
            test_suite_dict['test_cases'].append(test_case_dict)

        test_suites_list.append(test_suite_dict)

    return make_response({'test_suites': test_suites_list}, HTTPStatus.OK)


@test_suites.route('/new', methods=['POST'])
def new():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    name = request.json.get('name')
    description = request.json.get('description')
    test_case_ids = request.json.get('test_case_ids')

    if not all([name, description, test_case_ids]):
        msg = 'Required fields: name,description,test_case_ids'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    test_suite = TestSuite(
        project_id=user.active_project_id,
        name=name,
        description=description,
    )
    DBSession.add(test_suite)
    DBSession.commit()

    order = 1
    for test_case_id in test_case_ids:
        test_case_test_suite = TestCaseTestSuite(
            test_case_id=test_case_id,
            test_suite_id=test_suite.id,
            order=order,
        )
        DBSession.add(test_case_test_suite)
        order += 1
    DBSession.commit()

    return message_response(f'Successfully created test suite with id `{test_suite.id}`', HTTPStatus.CREATED)

