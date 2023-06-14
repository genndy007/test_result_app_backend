from http import HTTPStatus

from flask import request, make_response
from sqlalchemy import select

from src.api.auth.utils import get_current_user
from src.models import DBSession
from src.models.user import User
from src.models.test_case import TestCase, TestStep
from src.models.test_suite import TestRun, TestCaseTestRun, TestSuite
from src.utils import message_response
from . import test_runs


# todo: test steps left to load into response
@test_runs.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_suites_ids = [
        row[0] for row in DBSession.query(TestSuite.id).filter(TestSuite.project_id == user.active_project_id).all()
    ]

    test_runs_list = []
    test_runs_qs = DBSession.query(TestRun).filter(TestRun.test_suite_id.in_(test_suites_ids))
    for test_run in test_runs_qs:
        test_suite_qs = DBSession.query(TestSuite).filter(TestSuite.id == test_run.test_suite_id).first()
        test_run_dict = {
            'id': test_run.id,
            'result': test_run.result,
            'timestamp': test_run.created.strftime('%Y-%m-%d %H:%M:%S'),
            'test_suite': {
                'name': test_suite_qs.name,
                'description': test_suite_qs.description,
            },
            'test_cases': [],
        }

        test_cases_ids_results = DBSession.query(TestCaseTestRun.test_case_id, TestCaseTestRun.status)\
            .filter(TestCaseTestRun.test_run_id == test_run.id).all()
        for test_case_id_result in test_cases_ids_results:
            test_case_details = DBSession.query(TestCase).filter(TestCase.id == test_case_id_result[0]).first()
            test_case_dict = {
                'id': test_case_id_result[0],
                'name': test_case_details.name,
                'description': test_case_details.description,
                'status': test_case_id_result[1],
                'precondition': test_case_details.precondition,
                'postcondition': test_case_details.postcondition,
                'test_steps': []
            }
            test_run_dict['test_cases'].append(test_case_dict)

        test_runs_list.append(test_run_dict)

    return make_response({'test_runs': test_runs_list}, HTTPStatus.OK)

