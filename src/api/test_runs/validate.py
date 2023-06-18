

def validate_test_case_statuses(test_case_statuses):
    for test_case_status in test_case_statuses:
        if 'test_case_id' not in test_case_status or 'status' not in test_case_status:
            return False
    return True
