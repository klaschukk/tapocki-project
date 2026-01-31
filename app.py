from flask import Flask
from flask_login import LoginManager
from config import Config
from routes.main import main_bp
from routes.products import products_bp
from routes.auth import auth_bp
from routes.cart import cart_bp
from routes.admin import admin_bp
from database.db import db
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'


@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user_by_id(user_id)
    if user_data:
        return User(user_data)
    return None


# Регистрируем blueprints
app.register_blueprint(main_bp)
app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)

# Добавляем current_user в контекст всех шаблонов


@app.context_processor
def inject_user():
    from flask_login import current_user
    return dict(current_user=current_user)


if __name__ == '__main__':
    print("🚀 Запускаем Flask сервер...")
    print("📍 Главная страница: http://127.0.0.1:5000/")
    print("📍 Каталог: http://127.0.0.1:5000/products")
    print("📍 О нас: http://127.0.0.1:5000/about")
    print("📍 Вход: http://127.0.0.1:5000/login")
    print("📍 Регистрация: http://127.0.0.1:5000/register")
    print("📍 Админ-панель: http://127.0.0.1:5000/admin")
    app.run(debug=True, port=5000)
