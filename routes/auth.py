from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from database.db import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверяем существует ли пользователь
        existing_user = db.get_user_by_email(email)
        if existing_user:
            flash('Email уже зарегистрирован', 'error')
            return redirect(url_for('auth.register'))

        # Создаем пользователя
        user_data = User.create_user(email, username, password)
        user_id = db.create_user(user_data)

        flash('Регистрация успешна! Войдите в систему', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = db.get_user_by_email(email)

        if not user_data:
            flash('Неверный email или пароль', 'error')
            return redirect(url_for('auth.login'))

        user = User(user_data)

        if not user.check_password(password):
            flash('Неверный email или пароль', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Выход"""
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """Личный кабинет"""
    orders = db.get_user_orders(current_user.id)
    return render_template('profile.html', orders=orders)
