# Configuration settings for database access

import os

# SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///dev.db')

# JWT Secret key
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

# Flask/FastAPI settings
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Environment settings
ENV = os.getenv('ENV', 'development')

if ENV == 'production':
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY_PROD')
    DEBUG = False
