from flask import Blueprint, render_template, jsonify
from database.db import db

products_bp = Blueprint('products', __name__)


@products_bp.route('/products')
def products_page():
    """Страница каталога товаров"""
    products = db.get_all_products()
    return render_template('products.html', products=products)


@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Детальная страница товара"""
    product = db.get_product_by_id(product_id)

    if not product:
        return "Товар не найден", 404

    # Получаем похожие товары (другие товары из той же категории)
    related_products = db.get_products_by_category(product['categories'][0])
    # Исключаем текущий товар и берем максимум 3
    related_products = [
        p for p in related_products if p['id'] != product_id][:3]

    return render_template('product_detail.html', product=product, related=related_products)


@products_bp.route('/api/products')
def api_products():
    """API для получения всех товаров (JSON)"""
    products = db.get_all_products()
    # Удаляем _id из MongoDB (он не сериализуется в JSON)
    for product in products:
        product.pop('_id', None)
    return jsonify(products)


@products_bp.route('/api/product/<int:product_id>')
def api_product_detail(product_id):
    """API для получения одного товара (JSON)"""
    product = db.get_product_by_id(product_id)
    if product:
        product.pop('_id', None)
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404
