"""
Django settings for readitdown project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['RD_SECRET_KEY']

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
if ON_OPENSHIFT:
    DEBUG = bool(os.environ.get('DEBUG', False))
    if DEBUG:
        print("WARNING: The DEBUG environment is set to True.")
else:
    DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.readitdown.com',
    '.rhcloud.com',
]

if not ON_OPENSHIFT:
    ALLOWED_HOSTS.append('127.0.0.1')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'sslserver',
    'registration',
    'main',
    'access',
    'readingtracker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# GETTING-STARTED: change 'readitdown' to your project name:
ROOT_URLCONF = 'readitdown.urls'

WSGI_APPLICATION = 'readitdown.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.environ['OPENSHIFT_APP_NAME'],               # Or path to database file if using sqlite3.
            'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],               # Not used with sqlite3.
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],         # Not used with sqlite3.
            'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],               # Set to empty string for localhost. Not used with sqlite3.
            'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],               # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # GETTING-STARTED: change 'db.sqlite3' to your sqlite3 database:
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '../templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

SENTRY_HASH = os.environ['RD_SENTRY_HASH']
SENTRY_FIVE_DIGIT = os.environ['RD_SENTRY_FIVE_DIGIT']
RAVEN_CONFIG = { 'dsn': 'https://%s@app.getsentry.com/%s' % (SENTRY_HASH, SENTRY_FIVE_DIGIT), }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'readitdown'
EMAIL_HOST_PASSWORD = 'vols3131'
DEFAULT_FROM_EMAIL = 'readitdown@gmail.com'

ACCOUNT_ACTIVATION_DAYS = 250
REGISTRATION_DEFAULT_FROM_EMAIL = 'readitdown@gmail.com'
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_EMAIL_HTML = True

SITE_ID = 1
