import os
from dotenv import load_dotenv


load_dotenv()

# Global Debug
GLOBAL_DEBUG = os.getenv("GLOBAL_DEBUG")

# DB connection settings
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Django configuration
DJANGO_SECRET = os.getenv("DJANGO_SECRET")

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")
REDIS_DB = os.getenv("REDIS_DB")
