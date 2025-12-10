from .settings import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Permitir el host de Railway
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Permite todos los subdominios de Railway
]

# Database - PostgreSQL en producción
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuración de WhiteNoise para archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files - Cloudinary (lo configuraremos después)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Secret key desde variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-temporal')

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
]