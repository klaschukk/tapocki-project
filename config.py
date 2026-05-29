import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tapocki-dev-secret-2024'
    MONGO_URI = 'mongodb://localhost:27017/'  # unused — in-memory db
    DATABASE_NAME = 'slippers_db'
