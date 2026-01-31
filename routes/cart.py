from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database.db import db
from datetime import datetime

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@login_required
def view_cart():
    """Просмотр корзины"""
    cart_data = db.get_cart(current_user.id)
    items = cart_data.get('items', [])

    # Получаем полную информацию о товарах
    cart_items = []
    total = 0

    for item in items:
        product = db.get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
            total += item_total

    return render_template('cart.html', cart_items=cart_items, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Добавить товар в корзину"""
    quantity = int(request.form.get('quantity', 1))

    # Проверяем существует ли товар
    product = db.get_product_by_id(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('products.products_page'))

    db.add_to_cart(current_user.id, product_id, quantity)
    flash(f'{product["name"]} добавлен в корзину!', 'success')

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    """Обновить количество товара в корзине"""
    quantity = int(request.form.get('quantity', 1))

    if quantity <= 0:
        db.remove_from_cart(current_user.id, product_id)
    else:
        db.update_cart_item(current_user.id, product_id, quantity)

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/remove/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    """Удалить товар из корзины"""
    db.remove_from_cart(current_user.id, product_id)
    flash('Товар удален из корзины', 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/clear')
@login_required
def clear_cart():
    """Очистить корзину"""
    db.clear_cart(current_user.id)
    flash('Корзина очищена', 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Оформление заказа"""
    if request.method == 'POST':
        # Получаем корзину
        cart_data = db.get_cart(current_user.id)
        items = cart_data.get('items', [])

        if not items:
            flash('Корзина пуста', 'error')
            return redirect(url_for('cart.view_cart'))

        # Собираем данные о товарах
        order_items = []
        total = 0

        for item in items:
            product = db.get_product_by_id(item['product_id'])
            if product:
                item_total = product['price'] * item['quantity']
                order_items.append({
                    'product_id': item['product_id'],
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': item['quantity'],
                    'total': item_total
                })
                total += item_total

        # Данные доставки
        shipping_info = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'postal_code': request.form.get('postal_code')
        }

        # Создаем заказ
        order_data = {
            'user_id': current_user.id,
            'items': order_items,
            'total': total,
            'shipping_info': shipping_info,
            'status': 'pending',  # pending, processing, shipped, delivered, cancelled
            'created_at': datetime.now()
        }

        order_id = db.create_order(order_data)

        # Очищаем корзину
        db.clear_cart(current_user.id)

        flash('Заказ успешно оформлен!', 'success')
        return redirect(url_for('auth.profile'))

    # GET запрос - показываем форму оформления
    cart_data = db.get_cart(current_user.id)
    items = cart_data.get('items', [])

    cart_items = []
    total = 0

    for item in items:
        product = db.get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
            total += item_total

    return render_template('checkout.html', cart_items=cart_items, total=total)

# API для AJAX запросов


@cart_bp.route('/api/cart/count')
@login_required
def cart_count():
    """Получить количество товаров в корзине"""
    cart_data = db.get_cart(current_user.id)
    items = cart_data.get('items', [])
    count = sum(item['quantity'] for item in items)
    return jsonify({'count': count})
