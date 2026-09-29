from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'esra_storesql',
        'USER': 'postgres',
        'PASSWORD': 'esra3264',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}