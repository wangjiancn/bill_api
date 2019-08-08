import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))  # ../../path

# Envirnment
ENV_MONGO_USERNAME = os.environ.get('ENV_MONGO_USERNAME', 'root')
ENV_MONGO_PASSWORD = os.environ.get('ENV_MONGO_PASSWORD', '123456')
ENV_MONGO_HOST = os.environ.get('ENV_MONGO_HOST', '127.0.0.1')
ENV_MONGO_PORT = os.environ.get('ENV_MONGO_PORT', 27017)
ENV_MONGO_DATABASE_NAME = os.environ.get(
    'ENV_MONGO_DATABASE_NAME', 'test')
ENV_MAX_POOL_SIZE = os.environ.get('ENV_MAX_POOL_SIZE', 1)

ENV_UPLOAD_PATH = os.environ.get(
    'ENV_UPLOAD_PATH',
    os.path.join(os.path.dirname(BASE_DIR), 'media')  # ../../media
)

ENV_BLOG_SECRET_KEY = os.environ.get('ENV_BLOG_SECRET_KEY', 'secret_key')


SECRET_KEY = ENV_BLOG_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENV_DEBUG', 'true') == 'true'

ALLOWED_HOSTS = ['*']

MONGO_CONF = {
    'NAME': ENV_MONGO_DATABASE_NAME,
    'USER': ENV_MONGO_USERNAME,
    'PASSWORD': ENV_MONGO_PASSWORD,
    'HOST': ENV_MONGO_HOST,
    'PORT': ENV_MONGO_PORT,
    'MAX_POOL_SIZE': ENV_MAX_POOL_SIZE
}
