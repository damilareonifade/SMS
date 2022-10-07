
import os
import socket

import environ

env = environ.Env()
environ.Env.read_env()
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e%c^aoils5zoi!^!ojat9*y70jkh(n&o6b$trl8lo@pq4f+*ur'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'accounts',
    'crispy_forms',
    'finance',
    'django_mfa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'School management system',
        "USER":'postgres',
        'PASSWORD':'okay',
        'HOST':'localhost',
        'PORT':'5433',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR/'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#overriden user model
AUTH_USER_MODEL = 'accounts.CustomUser'

#crispy form
CRISPY_TEMPLATE_PACK = 'bootstrap4'
#backend Configuration


#media configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [BASE_DIR/"static/"]

MFA_UNALLOWED_METHODS=()   # Methods that shouldn't be allowed for the user
MFA_LOGIN_CALLBACK="accounts.views.login_user_in"            # A function that should be called by username to login the user in session
MFA_RECHECK=True           # Allow random rechecking of the user
MFA_RECHECK_MIN=10         # Minimum interval in seconds
MFA_RECHECK_MAX=30         # Maximum in seconds
MFA_QUICKLOGIN=True        # Allows quick login for returning users

TOKEN_ISSUER_NAME="SMS"      #TOTP Issuer name, this should be your project's name

if DEBUG:
  U2F_APPID="https://localhost"    #URL For U2F
  FIDO_SERVER_ID=u"localhost"      # Server rp id for FIDO2, it is the full domain of your project
else:
  U2F_APPID="https://django-mfa2-example.herokuapp.com"    #URL For U2F
  FIDO_SERVER_ID=u"django-mfa2-example.herokuapp.com"      # Server rp id for FIDO2, it is the full domain of your project

FIDO_SERVER_NAME=u"django_mfa2_example"
MFA_REDIRECT_AFTER_REGISTRATION = 'accounts:index'
MFA_SUCCESS_REGISTRATION_MSG = 'Your keys have successfully been created! You '


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
#Custom settings. To Email
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')

socket.getaddrinfo('127.0.0.1', 8000)