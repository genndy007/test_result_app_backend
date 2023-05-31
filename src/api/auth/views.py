from . import auth


@auth.route('/check')
def check():
    return "Check app works"


