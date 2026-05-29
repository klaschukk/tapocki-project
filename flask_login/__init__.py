"""Flask-Login stub backed by Flask sessions — no external dependency."""
from flask import session, redirect, url_for, request as _req
from functools import wraps


class UserMixin:
    @property
    def is_active(self): return True
    @property
    def is_anonymous(self): return False
    @property
    def is_authenticated(self): return True
    def get_id(self): return str(self.id)


class _CurrentUser:
    @property
    def is_authenticated(self):
        return 'user_id' in session

    @property
    def is_anonymous(self):
        return 'user_id' not in session

    @property
    def is_admin(self):
        return session.get('is_admin', False)

    @property
    def id(self):
        return session.get('user_id')

    @property
    def email(self):
        return session.get('user_email', '')

    @property
    def username(self):
        return session.get('username', '')

    def __bool__(self):
        return self.is_authenticated


current_user = _CurrentUser()


def login_user(user, remember=False):
    session['user_id'] = user.id
    session['is_admin'] = getattr(user, 'is_admin', False)
    session['user_email'] = getattr(user, 'email', '')
    session['username'] = getattr(user, 'username', '')
    session.permanent = remember


def logout_user():
    for k in ('user_id', 'is_admin', 'user_email', 'username'):
        session.pop(k, None)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=_req.url))
        return f(*args, **kwargs)
    return decorated


class LoginManager:
    login_view = None
    login_message = None

    def init_app(self, app):
        pass

    def user_loader(self, f):
        return f
