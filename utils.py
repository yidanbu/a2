from functools import wraps

import bcrypt
from flask import session, abort

def validate_password(password):
    pass

def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


def check_password(stored_password, user_input_password):
    return bcrypt.checkpw(user_input_password.encode('utf-8'), stored_password.encode('utf-8'))


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                abort(403)
            return func(*args, **kwargs)

        return decorated_function

    return decorator
