# -*- coding: utf-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), ".."))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monapay',
    'south',
    'rest_framework',
    'widget_tweaks',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'payment.urls'
WSGI_APPLICATION = 'payment.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'payment',
        'USER': 'payment',
        'PASSWORD': 'XXXXXXXX',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ja-JP'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('ja', gettext('Japanese')),
    ('en', gettext('English')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'deploy')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'monapay': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# e-mail settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.monapay.com'
    EMAIL_HOST_PASSWORD = 'XXXXXXXX'
    EMAIL_HOST_USER = 'XXXXXXXX@mail.monapay.com'
    EMAIL_USE_TLS = True

# rest-framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.XMLRenderer',
    )
}

# session settings
# We set the age of cookies to 2 weeks.
SESSION_COOKIE_AGE = 1209600

# PAYMENT specific settings
from decimal import Decimal
PAYMENT_DEFAULT_FEE = Decimal("0.01")
PAYMENT_TRANSACTION_FEE = Decimal("0.001")
PAYMENT_WALLET_ACCOUNT_NAME = "payment"
PAYMENT_FEE_ACCOUNT_NAME = "fee"
PAYMENT_MINIMUM_PRICE = Decimal("1.0")
PAYMENT_MAXIMUM_PRICE = Decimal("10000.0")
MONACOIND_ADMIN_USER = "rpcadmin"
MONACOIND_ADMIN_PASSWORD = "XXXXXXXX"
MONACOIND_HOST = "127.0.0.1"
MONACOIND_PORT = 30971
