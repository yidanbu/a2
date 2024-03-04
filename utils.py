from functools import wraps

import bcrypt
from flask import session, abort


def hash_password(password):
    # 将密码转换为bytes，然后生成盐和哈希
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed

def check_password(stored_password, user_input_password):
    return bcrypt.checkpw(user_input_password.encode('utf-8'), stored_password.encode('utf-8'))

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                # 如果用户角色不匹配，可以重定向到登录页面或返回错误
                abort(403)  # 或使用 redirect(url_for('login'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator