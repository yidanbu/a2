import re
from functools import wraps

import bcrypt
from flask import session, abort


def check_password(password):
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    if len(password) < 8:
        return False

    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    return has_lower and has_upper and has_digit and has_special


def check_email(email):
    pattern = r'\S+@\S+\.\S+'
    if not re.match(pattern, email):
        return False
    return True


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
