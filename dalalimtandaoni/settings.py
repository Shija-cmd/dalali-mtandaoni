import os

from dotenv import load_dotenv

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):

    return os.environ.get(
        name,
        str(default)
    ).lower() == 'true'


def env_int(name, default):

    return int(
        os.environ.get(
            name,
            default
        )
    )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool(
    'DJANGO_DEBUG',
    False
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    ''
)

if not SECRET_KEY:

    if DEBUG:

        SECRET_KEY = (
            'django-insecure-+tjxo(r^27injx3-xyt5$=^0x+ng!'
            '+w%=yr+2l&yv&#^2hx-8d'
        )

    else:

        raise ImproperlyConfigured(
            'Set DJANGO_SECRET_KEY before running in production.'
        )

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost,10.0.2.2'
).split(',')

ADMIN_URL = os.environ.get(
    'DJANGO_ADMIN_URL',
    'admin/'
)

if not ADMIN_URL.endswith('/'):

    ADMIN_URL = f'{ADMIN_URL}/'

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.environ.get(
        'DJANGO_CSRF_TRUSTED_ORIGINS',
        ''
    ).split(',')
    if origin
]

CONTACT_UNLOCK_FEE = env_int(
    'CONTACT_UNLOCK_FEE',
    500
)

CONTACT_UNLOCK_DAYS = env_int(
    'CONTACT_UNLOCK_DAYS',
    3
)


# Application definition

INSTALLED_APPS = [
    'cloudinary_storage',
    'cloudinary',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'accounts',
    'properties',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dalalimtandaoni.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'properties.context_processors.verification_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'dalalimtandaoni.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'accounts.User'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DJANGO_SERVE_MEDIA = env_bool(
    'DJANGO_SERVE_MEDIA',
    DEBUG
)

DJANGO_SERVE_STATIC = env_bool(
    'DJANGO_SERVE_STATIC',
    DEBUG
)

SECURE_SSL_REDIRECT = env_bool(
    'DJANGO_SECURE_SSL_REDIRECT',
    not DEBUG
)

SESSION_COOKIE_SECURE = env_bool(
    'DJANGO_SESSION_COOKIE_SECURE',
    not DEBUG
)

CSRF_COOKIE_SECURE = env_bool(
    'DJANGO_CSRF_COOKIE_SECURE',
    not DEBUG
)

SECURE_HSTS_SECONDS = int(
    os.environ.get(
        'DJANGO_SECURE_HSTS_SECONDS',
        '0' if DEBUG else '31536000'
    )
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS',
    not DEBUG
)

SECURE_HSTS_PRELOAD = env_bool(
    'DJANGO_SECURE_HSTS_PRELOAD',
    not DEBUG
)

SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
) if os.environ.get(
    'DJANGO_USE_X_FORWARDED_PROTO',
    'False'
).lower() == 'true' else None

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

REFERRER_POLICY = 'same-origin'

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False

DATA_UPLOAD_MAX_MEMORY_SIZE = int(
    os.environ.get(
        'DJANGO_DATA_UPLOAD_MAX_MEMORY_SIZE',
        str(10 * 1024 * 1024)
    )
)

FILE_UPLOAD_MAX_MEMORY_SIZE = int(
    os.environ.get(
        'DJANGO_FILE_UPLOAD_MAX_MEMORY_SIZE',
        str(5 * 1024 * 1024)
    )
)

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [

        'rest_framework.authentication.TokenAuthentication',

    ],

    'DEFAULT_PERMISSION_CLASSES': [

        'rest_framework.permissions.AllowAny',

    ],

}

# Cloudinary Storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}