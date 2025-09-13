import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL configuration
    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_ORIGINS = ["*"]
    
    # Push notification settings
    MAX_PUSH_LENGTH = 160
    CURRENCY = 'KZT'
