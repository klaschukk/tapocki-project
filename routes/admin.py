from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from database.db import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('У вас нет прав доступа', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Главная страница админки"""
    products = db.get_all_products()
    orders = db.get_all_orders()

    # Статистика
    total_products = len(products)
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o['status'] == 'pending'])
    total_revenue = sum(o['total']
                        for o in orders if o['status'] != 'cancelled')

    stats = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue
    }

    recent_orders = orders[:5]  # Последние 5 заказов

    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """Управление товарами"""
    products = db.get_all_products()
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """Добавить товар"""
    if request.method == 'POST':
        # Получаем последний ID
        all_products = db.get_all_products()
        next_id = max([p['id'] for p in all_products]) + \
            1 if all_products else 1

        product_data = {
            'id': next_id,
            'name': request.form.get('name'),
            'slug': request.form.get('slug'),
            'category': request.form.get('category'),
            'categories': request.form.getlist('categories'),
            'price': int(request.form.get('price')),
            'badge': request.form.get('badge'),
            'badge_color': request.form.get('badge_color', 'green'),
            'rating': float(request.form.get('rating', 4.5)),
            'reviews_count': int(request.form.get('reviews_count', 0)),
            'description': request.form.get('description'),
            'images': ['🩴', '👟', '⚡', '✨'],  # Можно будет заменить
            'gradient': request.form.get('gradient'),
            'sizes': list(range(36, 46)),
            'unavailable_sizes': [],
            'colors': [
                {'name': 'purple',
                    'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}
            ],
            'features': [
                {'icon': '☁️', 'title': 'Облачный комфорт', 'description': 'Описание'}
            ],
            'specifications': {
                'Материал верха': 'Синтетический текстиль',
                'Материал подошвы': 'EVA пена',
                'Вес (размер 40)': '120 грамм',
                'Страна производства': 'Италия',
                'Гарантия': '12 месяцев'
            }
        }

        collection = db.get_collection('products')
        collection.insert_one(product_data)

        flash('Товар добавлен!', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/add_product.html')


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Редактировать товар"""
    product = db.get_product_by_id(product_id)

    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('admin.products'))

    if request.method == 'POST':
        update_data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': int(request.form.get('price')),
            'description': request.form.get('description'),
            'badge': request.form.get('badge')
        }

        db.update_product(product_id, update_data)
        flash('Товар обновлен!', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/edit_product.html', product=product)


@admin_bp.route('/products/delete/<int:product_id>')
@login_required
@admin_required
def delete_product(product_id):
    """Удалить товар"""
    db.delete_product(product_id)
    flash('Товар удален', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """Управление заказами"""
    all_orders = db.get_all_orders()

    # Добавляем информацию о пользователе к каждому заказу
    for order in all_orders:
        user = db.get_user_by_id(order['user_id'])
        if user:
            order['user_email'] = user.get('email', 'Неизвестен')
        else:
            order['user_email'] = 'Удалённый пользователь'

    return render_template('admin/orders.html', orders=all_orders)


@admin_bp.route('/orders/<order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """Обновить статус заказа"""
    new_status = request.form.get('status')
    db.update_order_status(order_id, new_status)
    flash('Статус заказа обновлен', 'success')
    return redirect(url_for('admin.orders'))
