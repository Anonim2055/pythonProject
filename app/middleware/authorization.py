from flask import session,url_for,redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('_id') is None:
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function