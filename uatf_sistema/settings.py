"""
Django settings for uatf_sistema project.
Configuración optimizada para Railway
"""

import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-desarrollo-local-cambiar')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Configuración de ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# En producción, agregar dominios de Railway
if not DEBUG:
    ALLOWED_HOSTS.extend([
        'uatf-sistema-production.up.railway.app',
        '.railway.app',
        '.up.railway.app',
    ])

# Si hay una variable de entorno RAILWAY_PUBLIC_DOMAIN, agregarla
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'gestion_carreras',
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

ROOT_URLCONF = 'uatf_sistema.urls'

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

WSGI_APPLICATION = 'uatf_sistema.wsgi.application'

# Database
# Por defecto usa SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si existe DATABASE_URL (Railway), usar PostgreSQL
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )

# Password validation
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
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuración de WhiteNoise para servir archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary Configuration (para archivos en producción)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# Usar Cloudinary solo en producción (cuando DEBUG=False)
if not DEBUG and CLOUDINARY_STORAGE['CLOUD_NAME']:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Login URLs
LOGIN_REDIRECT_URL = '/carreras/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Security settings for production
if not DEBUG:
    # IMPORTANTE: NO usar SECURE_SSL_REDIRECT en Railway
    # Esto causa un redirect loop infinito
    # SECURE_SSL_REDIRECT = True  ← NO DESCOMENTAR
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Security Headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # CSRF Settings - IMPORTANTE para Railway
    CSRF_TRUSTED_ORIGINS = [
        'https://uatf-sistema-production.up.railway.app',
        'https://*.railway.app',
        'https://*.up.railway.app',
    ]

# Asegurar que existan las carpetas necesarias en desarrollo
if DEBUG:
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    if not os.path.exists(STATIC_ROOT):
        os.makedirs(STATIC_ROOT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'