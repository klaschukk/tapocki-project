from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config


class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DATABASE_NAME]

    def get_collection(self, collection_name):
        """Получить коллекцию из БД"""
        return self.db[collection_name]

    # ========== PRODUCTS ==========
    def get_all_products(self):
        """Получить все товары"""
        products = self.db.products
        return list(products.find())

    def get_product_by_id(self, product_id):
        """Получить товар по ID"""
        products = self.db.products
        return products.find_one({"id": int(product_id)})

    def get_products_by_category(self, category):
        """Получить товары по категории"""
        products = self.db.products
        return list(products.find({"categories": category}))

    def insert_products(self, products_data):
        """Добавить товары в БД"""
        products = self.db.products
        products.delete_many({})
        if products_data:
            products.insert_many(products_data)
            return True
        return False

    def update_product(self, product_id, update_data):
        """Обновить товар"""
        products = self.db.products
        return products.update_one(
            {"id": int(product_id)},
            {"$set": update_data}
        )

    def delete_product(self, product_id):
        """Удалить товар"""
        products = self.db.products
        return products.delete_one({"id": int(product_id)})

    # ========== USERS ==========
    def create_user(self, user_data):
        """Создать пользователя"""
        users = self.db.users
        result = users.insert_one(user_data)
        return result.inserted_id

    def get_user_by_email(self, email):
        """Получить пользователя по email"""
        users = self.db.users
        return users.find_one({"email": email})

    def get_user_by_id(self, user_id):
        """Получить пользователя по ID"""
        users = self.db.users
        try:
            return users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    # ========== CART ==========
    def get_cart(self, user_id):
        """Получить корзину пользователя"""
        cart = self.db.cart
        user_cart = cart.find_one({"user_id": user_id})
        if not user_cart:
            # Создаем пустую корзину
            cart.insert_one({"user_id": user_id, "items": []})
            return {"user_id": user_id, "items": []}
        return user_cart

    def add_to_cart(self, user_id, product_id, quantity=1):
        """Добавить товар в корзину"""
        cart = self.db.cart
        user_cart = self.get_cart(user_id)

        # Проверяем есть ли уже товар в корзине
        items = user_cart.get('items', [])
        found = False

        for item in items:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                found = True
                break

        if not found:
            items.append({
                'product_id': product_id,
                'quantity': quantity
            })

        cart.update_one(
            {"user_id": user_id},
            {"$set": {"items": items}}
        )
        return True

    def update_cart_item(self, user_id, product_id, quantity):
        """Обновить количество товара в корзине"""
        cart = self.db.cart
        user_cart = self.get_cart(user_id)
        items = user_cart.get('items', [])

        for item in items:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                break

        cart.update_one(
            {"user_id": user_id},
            {"$set": {"items": items}}
        )
        return True

    def remove_from_cart(self, user_id, product_id):
        """Удалить товар из корзины"""
        cart = self.db.cart
        user_cart = self.get_cart(user_id)
        items = user_cart.get('items', [])

        items = [item for item in items if item['product_id'] != product_id]

        cart.update_one(
            {"user_id": user_id},
            {"$set": {"items": items}}
        )
        return True

    def clear_cart(self, user_id):
        """Очистить корзину"""
        cart = self.db.cart
        cart.update_one(
            {"user_id": user_id},
            {"$set": {"items": []}}
        )
        return True

    # ========== ORDERS ==========
    def create_order(self, order_data):
        """Создать заказ"""
        orders = self.db.orders
        result = orders.insert_one(order_data)
        return result.inserted_id

    def get_user_orders(self, user_id):
        """Получить заказы пользователя"""
        orders = self.db.orders
        return list(orders.find({"user_id": user_id}).sort("created_at", -1))

    def get_all_orders(self):
        """Получить все заказы (для админа)"""
        orders = self.db.orders
        return list(orders.find().sort("created_at", -1))

    def get_order_by_id(self, order_id):
        """Получить заказ по ID"""
        orders = self.db.orders
        try:
            return orders.find_one({"_id": ObjectId(order_id)})
        except:
            return None

    def update_order_status(self, order_id, status):
        """Обновить статус заказа"""
        orders = self.db.orders
        try:
            return orders.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": {"status": status}}
            )
        except:
            return None


# Создаем глобальный экземпляр
db = Database()
