from http import HTTPStatus

from flask import request, make_response
from sqlalchemy import select

from src.api.auth.utils import get_current_user
from src.models import DBSession
from src.models.user import User
from src.models.test_case import TestCase, TestStep
from src.models.test_suite import TestRun, TestCaseTestRun, TestSuite
from src.utils import message_response
from .db import get_test_run_by_id
from . import test_runs
from src.core.pdf.report import TestRunReportPDF
from ...core.pdf.upload import SingletonFilestack


@test_runs.route('/list_my', methods=['GET'])
def list_my():
    user = get_current_user(request)
    if not user:
        return message_response('Authenticate at /auth/login first', HTTPStatus.FORBIDDEN)

    test_suites_qs = DBSession.query(TestSuite.id).filter(TestSuite.project_id == user.active_project_id)
    test_suites_ids = [row[0] for row in test_suites_qs]

    test_runs_list = []
    test_runs_qs = DBSession.query(TestRun).filter(TestRun.test_suite_id.in_(test_suites_ids))
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
