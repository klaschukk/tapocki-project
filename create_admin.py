from database.db import db
from models.user import User


def create_admin():
    """Создать админа"""
    email = "admin@balconyslippers.com"
    username = "admin"
    password = "admin123"  # Смени потом!

    # Проверяем существует ли
    existing = db.get_user_by_email(email)
    if existing:
        print("❌ Админ уже существует!")
        return

    # Создаем
    user_data = User.create_user(email, username, password, is_admin=True)
    user_id = db.create_user(user_data)

    print("✅ Админ создан!")
    print(f"📧 Email: {email}")
    print(f"🔑 Пароль: {password}")
    print("⚠️  Обязательно смени пароль после первого входа!")


if __name__ == "__main__":
    create_admin()
