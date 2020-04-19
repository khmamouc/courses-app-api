from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'appbase',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'pwd',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = []
ALLOWED_HOSTS = ['0.0.0.0']

DEBUG = True
CACHALOT_ENABLED = True