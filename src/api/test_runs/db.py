from src.models import DBSession
from src.models.test_case import TestCase, TestStep
from src.models.test_suite import TestRun, TestCaseTestRun, TestSuite


def get_test_run_by_id(test_run_id):
    test_run = DBSession.query(TestRun).filter(TestRun.id == test_run_id).first()
    if not test_run:
        return {}

    test_suite_qs = DBSession.query(TestSuite).filter(TestSuite.id == test_run.test_suite_id).first()
    test_run_dict = {
        'id': test_run.id,
        'result': test_run.result,
        'timestamp': test_run.created.strftime('%Y-%m-%d %H-%M-%S'),
        'test_suite': {
            'name': test_suite_qs.name,
            'description': test_suite_qs.description,
        },
        'test_cases': [],
    }

    test_cases_ids_results = DBSession.query(TestCaseTestRun.test_case_id, TestCaseTestRun.status) \
        .filter(TestCaseTestRun.test_run_id == test_run.id).all()
    for test_case_id_result in test_cases_ids_results:
        test_case_id, test_case_result = test_case_id_result
        test_case_details = DBSession.query(TestCase).filter(TestCase.id == test_case_id).first()
        test_case_dict = {
            'id': test_case_id,
            'name': test_case_details.name,
            'description': test_case_details.description,
            'status': test_case_result,
            'precondition': test_case_details.precondition,
            'postcondition': test_case_details.postcondition,
            'test_steps': []
        }

        test_steps_qs = DBSession.query(TestStep).filter(TestStep.test_case_id == test_case_id).order_by(TestStep.order)
        for test_step in test_steps_qs:
            test_step_dict = {
                'content': test_step.content,
                'order': test_step.order,
            }
            test_case_dict['test_steps'].append(test_step_dict)

        test_run_dict['test_cases'].append(test_case_dict)

    return test_run_dict
