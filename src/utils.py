from flask import make_response


def message_response(message, code):
    return make_response({'message': message}, code)
