from http import HTTPStatus

from flask import request, make_response

from src.api.auth.utils import get_current_user
from src.core.pdf.report import TestRunReportPDF
from src.core.pdf.upload import SingletonFilestack
from src.models import DBSession
from src.models.test_suite import TestRun, TestCaseTestRun, TestSuite, TestCaseTestSuite
from src.utils import message_response
from . import test_runs
from .db import get_test_run_by_id
from .validate import validate_test_case_statuses


@test_runs.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_suites_qs = DBSession.query(TestSuite.id).filter(TestSuite.project_id == user.active_project_id)
    test_suites_ids = [row[0] for row in test_suites_qs]

    test_runs_list = []
    test_runs_qs = DBSession.query(TestRun)\
        .filter(TestRun.test_suite_id.in_(test_suites_ids))\
        .order_by(TestRun.id.desc())
    for test_run in test_runs_qs:
        test_run_dict = get_test_run_by_id(test_run.id)
        test_runs_list.append(test_run_dict)

    return make_response({'test_runs': test_runs_list}, HTTPStatus.OK)


@test_runs.route('/<int:test_run_id>/report', methods=['GET'])
def id_report(test_run_id):
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_run_dict = get_test_run_by_id(test_run_id)
    report_path = TestRunReportPDF(test_run_dict).make()
    report_url = SingletonFilestack().upload_pdf(report_path)

    return make_response({'report_url': report_url}, HTTPStatus.OK)


@test_runs.route('/new', methods=['POST'])
def new():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_suite_id = request.json.get('test_suite_id')
    result = request.json.get('result')
    test_case_statuses = request.json.get('test_case_statuses')

    if not all([test_suite_id, result, test_case_statuses]):
        msg = 'Required fields: test_suite_id,result,test_case_statuses'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    if not validate_test_case_statuses(test_case_statuses):
        msg = 'Each test_case_status must contain: test_case_id,status'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    all_needed_test_case_ids_qs = DBSession.query(TestCaseTestSuite.test_case_id)\
        .distinct(TestCaseTestSuite.test_case_id)\
        .filter(TestCaseTestSuite.test_suite_id == test_suite_id)
    all_needed_test_case_ids = set(row[0] for row in all_needed_test_case_ids_qs)
    got_test_case_ids = set(row['test_case_id'] for row in test_case_statuses)

    if got_test_case_ids != all_needed_test_case_ids:
        msg = f'Need test case ids: {all_needed_test_case_ids}, got {got_test_case_ids}'
        return message_response(msg, HTTPStatus.BAD_REQUEST)

    test_run = TestRun(
        test_suite_id=test_suite_id,
        result=result,
    )
    DBSession.add(test_run)
    DBSession.commit()

    for test_case_status in test_case_statuses:
        test_case_test_run = TestCaseTestRun(
            test_run_id=test_run.id,
            test_case_id=test_case_status['test_case_id'],
            status=test_case_status['status'],
        )
        DBSession.add(test_case_test_run)
    DBSession.commit()

    return message_response(f'Successfully created Test Run with id `{test_run.id}`', HTTPStatus.CREATED)
