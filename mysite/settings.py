import base64
import os
from pathlib import Path
from os.path import join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Security
# ------------------------------
SECRET_KEY = 'django-insecure-5c7drgu&8_=e48&$rg)ptm_l&i-z*u(mw^2_@8xtf0w@3%$ntk'
DEBUG = True
ALLOWED_HOSTS = []

# ------------------------------
# Installed apps & middleware
# ------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'widget_tweaks',
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

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ------------------------------
# Database
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------
# Password validation
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------
# Static & media files
# ------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [join(BASE_DIR / 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'index'

# ------------------------------
# Storage (S3 example)
# ------------------------------


# ------------------------------
# Encryption Keys
# ------------------------------
# django-encrypted-model-fields
FIELD_ENCRYPTION_KEY = base64.urlsafe_b64encode(os.urandom(32))

# Fernet key for encrypted file storage
FERNET_KEY = b'vaY3x_tmBHtV3YtlAqwP2AhfY8YGef4WXDNg-8hEbE0='

# For production:
# FERNET_KEY = os.environ.get('FERNET_KEY')
# FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY')
