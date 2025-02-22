import os
import dj_database_url
from pathlib import Path
import environ


# Load environment variables
env = environ.Env()
environ.Env.read_env()  # Reads variables from .env file


# Security Settings
SECRET_KEY = env('SECRET_KEY', default='fallback-dev-key')
DEBUG = env.bool('DEBUG', default=True)  # Set to False in production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.herokuapp.com', 'localhost', '127.0.0.1'])


AUTH_USER_MODEL = 'useraccounts.CustomUser'

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent


ACCOUNT_FORMS = {
    'signup': 'useraccounts.forms.CustomSignupForm'
}

# Installed Apps
INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'django.contrib.sites',


   'allauth',
   'allauth.account',
   'allauth.socialaccount',
   'allauth.socialaccount.providers.google',
]


# Middleware
MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'allauth.account.middleware.AccountMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
   'allauth.account.middleware.AccountMiddleware',
]


# Authentication Backends
AUTHENTICATION_BACKENDS = [
   'django.contrib.auth.backends.ModelBackend',
   'allauth.account.auth_backends.AuthenticationBackend',  # Needed for django-allauth
]


# URLs
ROOT_URLCONF = 'projectb18.urls'


# Templates Configuration
TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [BASE_DIR / "templates"], 
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


# WSGI Application
WSGI_APPLICATION = 'projectb18.wsgi.application'


# Database Configuration (Heroku & Local)
DATABASES = {
   'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}


# Authentication Settings for django-allauth
SITE_ID = 6


SOCIALACCOUNT_ADAPTER = "projectb18.adapters.MySocialAccountAdapter"


SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ASSOCIATE_BY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True


LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"


ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"


# Password validation
AUTH_PASSWORD_VALIDATORS = [
   {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
   {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
   {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
   {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static Files Configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Heroku Deployment Compatibility
try:
   if 'HEROKU' in os.environ:
       import django_heroku
       django_heroku.settings(locals())
except ImportError:
   pass