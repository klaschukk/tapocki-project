from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('id', user_data.get('_id', '')))
        self.email = user_data.get('email', '')
        self.username = user_data.get('username', '')
        self.password_hash = user_data.get('password_hash', '')
        self.is_admin = user_data.get('is_admin', False)
        self.created_at = user_data.get('created_at', datetime.now())

    @staticmethod
    def create_user(email, username, password, is_admin=False):
        return {
            'email': email,
            'username': username,
            'password_hash': generate_password_hash(password, method='pbkdf2:sha256'),
            'is_admin': is_admin,
            'created_at': datetime.now(),
        }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id
