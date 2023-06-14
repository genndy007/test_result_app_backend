

def validate_test_steps(test_steps):
    for test_step in test_steps:
        if 'content' not in test_step or 'order' not in test_step:
            return False
        if type(test_step['order']) is not int:
            return False
    return True
