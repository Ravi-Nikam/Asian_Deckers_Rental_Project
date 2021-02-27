"""
Django settings for asian_decoration project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c(q4r+osr2(plg9ld%au9&qn*%!rhmzir-rj=l!6&gw@&ac_k)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# email
ALLOWED_HOSTS = []

DEFAULT_FROM_EMAIL = "someemail@gmail.com"

EMAIL_HOST = 'smtp.gmail.com'   #'smtp.sendgrid.net'  # its email servce
EMAIL_HOST_USER = ''   # login to gmail  os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = ''        # password of it  os.environ.get('EMAIL_PASS')
EMAIL_PORT = 587                               #
EMAIL_USE_TLS = True

# for password reser and forgot
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# tag library for reset passwword


# site url
SITE_URL = "http://cfestore.com"
if DEBUG:
    SITE_URL = "http://127.0.0.1:8000"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dec_app',
    'cart_app',
    'order',
    'accounts',
    'localflavor',
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asian_decoration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'asian_decoration.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME'  : 'asian_dec',
        'USER'  : 'postgres',
        'PASSWORD' :'1234',
        'HOST' : 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/videos/"
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')


STRIPE_SECRET_KEY = "sk_test_CQP5LhOnpbn5VITmtZwlVJQl00bBk87knN"
STRIPE_PUBLISHABLE_KEY = "pk_test_G4HO8EoSD5WoUr3vrjubgiaN0084QJU7aD"
