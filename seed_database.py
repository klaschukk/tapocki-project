from database.db import db

# Данные для всех 5 товаров
products_data = [
    {
        "id": 1,
        "name": "Classic Comfort",
        "slug": "classic-comfort",
        "category": "Классическая коллекция",
        "categories": ["classic", "all"],  # Для фильтров
        "price": 2990,
        "badge": "Хит продаж",
        "badge_color": "green",
        "rating": 4.9,
        "reviews_count": 287,
        "description": "Идеальные тапочки для ежедневного использования на балконе. Мягкая подошва из пеноматериала обеспечивает максимальный комфорт, а дышащий материал позволяет ногам оставаться свежими весь день.",
        # Временно эмодзи, потом заменим на пути к файлам
        "images": ["🩴", "👟", "⚡", "✨"],
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "sizes": [36, 37, 38, 39, 40, 41, 42, 44, 45],
        "unavailable_sizes": [43],
        "colors": [
            {"name": "purple",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
            {"name": "pink",
                "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
            {"name": "blue",
                "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"},
            {"name": "green",
                "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"}
        ],
        "features": [
            {
                "icon": "☁️",
                "title": "Облачная подошва",
                "description": "Специальная пена с эффектом памяти адаптируется под форму вашей стопы"
            },
            {
                "icon": "🌬️",
                "title": "Дышащий материал",
                "description": "Микроперфорация обеспечивает постоянную циркуляцию воздуха"
            },
            {
                "icon": "🛡️",
                "title": "Противоскользящая подошва",
                "description": "Специальный рисунок протектора гарантирует безопасность на влажных поверхностях"
            },
            {
                "icon": "♻️",
                "title": "Эко-материалы",
                "description": "100% перерабатываемые материалы, безопасные для окружающей среды"
            }
        ],
        "specifications": {
            "Материал верха": "Синтетический текстиль",
            "Материал подошвы": "EVA пена с памятью",
            "Вес (размер 40)": "120 грамм",
            "Толщина подошвы": "2.5 см",
            "Страна производства": "Италия",
            "Гарантия": "12 месяцев"
        }
    },
    {
        "id": 2,
        "name": "Premium Luxury",
        "slug": "premium-luxury",
        "category": "Премиум линия",
        "categories": ["premium", "all"],
        "price": 4990,
        "badge": "Премиум",
        "badge_color": "gold",
        "rating": 5.0,
        "reviews_count": 142,
        "description": "Топовая модель с memory foam подошвой и дизайнерским оформлением. Создана для тех, кто ценит роскошь в каждой детали.",
        "images": ["👟", "🩴", "⚡", "✨"],
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "sizes": [36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
        "unavailable_sizes": [],
        "colors": [
            {"name": "pink",
                "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
            {"name": "purple",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
            {"name": "gold",
                "gradient": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)"}
        ],
        "features": [
            {
                "icon": "💎",
                "title": "Premium материалы",
                "description": "Итальянская кожа высшего качества"
            },
            {
                "icon": "🧠",
                "title": "Memory Foam",
                "description": "Подошва запоминает форму вашей стопы"
            },
            {
                "icon": "✨",
                "title": "Дизайнерское исполнение",
                "description": "Уникальный дизайн от европейских мастеров"
            },
            {
                "icon": "🎁",
                "title": "Премиум упаковка",
                "description": "Поставляется в подарочной коробке"
            }
        ],
        "specifications": {
            "Материал верха": "Натуральная кожа",
            "Материал подошвы": "Memory Foam + TPU",
            "Вес (размер 40)": "150 грамм",
            "Толщина подошвы": "3 см",
            "Страна производства": "Италия",
            "Гарантия": "24 месяца"
        }
    },
    {
        "id": 3,
        "name": "Active Sport",
        "slug": "active-sport",
        "category": "Спортивная серия",
        "categories": ["sport", "new", "all"],
        "price": 3490,
        "badge": "Новинка",
        "badge_color": "blue",
        "rating": 4.8,
        "reviews_count": 95,
        "description": "Для активных людей. Усиленная фиксация стопы и противоскользящая подошва делают эти тапочки идеальными для любой активности.",
        "images": ["⚡", "👟", "🩴", "✨"],
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "sizes": [38, 39, 40, 41, 42, 43, 44, 45, 46],
        "unavailable_sizes": [46],
        "colors": [
            {"name": "blue",
                "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"},
            {"name": "black",
                "gradient": "linear-gradient(135deg, #434343 0%, #000000 100%)"},
            {"name": "red",
                "gradient": "linear-gradient(135deg, #f85032 0%, #e73827 100%)"}
        ],
        "features": [
            {
                "icon": "🏃",
                "title": "Спортивная подошва",
                "description": "Усиленная амортизация для активности"
            },
            {
                "icon": "🔒",
                "title": "Фиксация стопы",
                "description": "Регулируемые ремешки для надежной посадки"
            },
            {
                "icon": "💨",
                "title": "Вентиляция",
                "description": "Система воздушных каналов"
            },
            {
                "icon": "🌧️",
                "title": "Водоотталкивающая",
                "description": "Не боится влаги и дождя"
            }
        ],
        "specifications": {
            "Материал верха": "Синтетическая сетка",
            "Материал подошвы": "TPU + резина",
            "Вес (размер 40)": "180 грамм",
            "Толщина подошвы": "3.5 см",
            "Страна производства": "Германия",
            "Гарантия": "12 месяцев"
        }
    },
    {
        "id": 4,
        "name": "Eco Natural",
        "slug": "eco-natural",
        "category": "Эко-серия",
        "categories": ["classic", "new", "all"],
        "price": 3790,
        "badge": "Эко",
        "badge_color": "green",
        "rating": 4.7,
        "reviews_count": 128,
        "description": "100% натуральные материалы. Биоразлагаемая подошва и органический хлопок для тех, кто заботится о планете.",
        "images": ["🌿", "🩴", "👟", "✨"],
        "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "sizes": [36, 37, 38, 39, 40, 41, 42, 43, 44],
        "unavailable_sizes": [],
        "colors": [
            {"name": "green",
                "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"},
            {"name": "beige",
                "gradient": "linear-gradient(135deg, #d4a574 0%, #c9a876 100%)"},
            {"name": "white",
                "gradient": "linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)"}
        ],
        "features": [
            {
                "icon": "🌱",
                "title": "100% натуральные",
                "description": "Органический хлопок и бамбуковое волокно"
            },
            {
                "icon": "♻️",
                "title": "Биоразлагаемая",
                "description": "Полностью разлагается за 2 года"
            },
            {
                "icon": "🌍",
                "title": "Углеродно-нейтральная",
                "description": "Производство компенсирует выбросы CO2"
            },
            {
                "icon": "🌳",
                "title": "Сажаем деревья",
                "description": "С каждой парой мы сажаем 5 деревьев"
            }
        ],
        "specifications": {
            "Материал верха": "Органический хлопок",
            "Материал подошвы": "Натуральная пробка + каучук",
            "Вес (размер 40)": "110 грамм",
            "Толщина подошвы": "2 см",
            "Страна производства": "Португалия",
            "Гарантия": "12 месяцев"
        }
    },
    {
        "id": 5,
        "name": "Luxury Limited",
        "slug": "luxury-limited",
        "category": "Лимитированная серия",
        "categories": ["premium", "new", "all"],
        "price": 7990,
        "badge": "Limited",
        "badge_color": "gold",
        "rating": 5.0,
        "reviews_count": 43,
        "description": "Эксклюзивная модель с кристаллами Swarovski. Всего 100 пар в коллекции. Для тех, кто хочет выделиться.",
        "images": ["✨", "💎", "👑", "🩴"],
        "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "sizes": [36, 37, 38, 39, 40, 41, 42],
        "unavailable_sizes": [42],
        "colors": [
            {"name": "gold",
                "gradient": "linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)"},
            {"name": "silver",
                "gradient": "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)"},
            {"name": "rose",
                "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"}
        ],
        "features": [
            {
                "icon": "💎",
                "title": "Кристаллы Swarovski",
                "description": "Ручная инкрустация драгоценными кристаллами"
            },
            {
                "icon": "👑",
                "title": "Лимитированная серия",
                "description": "Всего 100 пар, каждая пронумерована"
            },
            {
                "icon": "🎨",
                "title": "Ручная работа",
                "description": "Изготовлено вручную итальянскими мастерами"
            },
            {
                "icon": "📜",
                "title": "Сертификат",
                "description": "Сертификат подлинности и уникальный номер"
            }
        ],
        "specifications": {
            "Материал верха": "Шелк + кожа",
            "Материал подошвы": "Кожа + позолота",
            "Вес (размер 40)": "140 грамм",
            "Толщина подошвы": "2.5 см",
            "Страна производства": "Италия",
            "Гарантия": "Пожизненная"
        }
    }
]


def seed_database():
    """Заполнить БД начальными данными"""
    print("🌱 Начинаем заполнение базы данных...")

    try:
        result = db.insert_products(products_data)
        if result:
            print(f"✅ Успешно добавлено {len(products_data)} товаров!")

            # Проверяем что данные добавились
            all_products = db.get_all_products()
            print(f"📦 Всего товаров в БД: {len(all_products)}")

            for product in all_products:
                print(f"  - {product['name']} ({product['price']} ₽)")
        else:
            print("❌ Ошибка при добавлении товаров")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    seed_database()
