# To debug the instance
import os
DEBUG = os.getenv('DEBUG_MODE', True)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

DB_SORTING_LOCALE = os.getenv('DB_SORTING_LOCALE', 'es_ES.utf8')
# Base connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'vetgt'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

HOST_IP = '127.0.0.1'
HOST_DOMAIN = 'http://'+os.getenv('HOST', '127.0.0.1')
INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = [os.getenv('HOST', '127.0.0.1')]


# Instance info
INSTANCE_COUNTRY = 'Guatemala'

# Phone default label
INSTANCE_DEFAULT_PHONE_LABEL = 'HOME'

# Map start location
MAP_START_LOCATION = 'Ciudad de Guatemala'

# General configuration
TIME_ZONE = 'America/Guatemala'
LANGUAGE_CODE = 'es'
