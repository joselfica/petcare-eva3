"""
============================================================================
Configuración del proyecto Django — PetCare EVA3
----------------------------------------------------------------------------
Archivo: petcare/settings.py
Propósito:
    Centraliza la configuración del proyecto Django: rutas base, apps
    instaladas, middleware, conexión a PostgreSQL, internacionalización,
    archivos estáticos, autenticación y parámetros de Django REST Framework.

Convenciones:
    - Valores sensibles (SECRET_KEY, credenciales BD) se leen desde
      variables de entorno mediante `python-decouple`.
    - `.env` (no versionado) contiene valores reales.
    - `.env.example` (versionado) sirve como plantilla.
============================================================================
"""

from pathlib import Path
from decouple import config, Csv

# ============================================================================
# RUTAS BASE
# ----------------------------------------------------------------------------
# BASE_DIR apunta a la raíz del proyecto (donde está manage.py).
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================================
# SEGURIDAD
# ----------------------------------------------------------------------------
# SECRET_KEY: clave criptográfica para firmar sesiones, CSRF y mensajes.
# DEBUG: en producción (AWS EC2) DEBE ser False.
# ALLOWED_HOSTS: dominios/IPs aceptados. En EC2 se agrega la IP pública.
# ============================================================================
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# ============================================================================
# APLICACIONES INSTALADAS
# ----------------------------------------------------------------------------
# Apps nativas + DRF (requerido por el enunciado) + app de dominio `clinica`.
# ============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',

    # Proyecto
    'clinica',
]


# ============================================================================
# MIDDLEWARE
# ----------------------------------------------------------------------------
# Orden crítico: Security → Session → Auth → CSRF.
# ============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================================
# URLS Y WSGI
# ============================================================================
ROOT_URLCONF = 'petcare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Carpeta global para templates compartidos (base, login, admin override)
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'petcare.wsgi.application'


# ============================================================================
# BASE DE DATOS — PostgreSQL
# ----------------------------------------------------------------------------
# Configuración vía variables de entorno. En EC2, PostgreSQL corre en la
# misma instancia, por lo que DB_HOST=localhost también aplica.
# ============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


# ============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================================
# INTERNACIONALIZACIÓN (Chile)
# ============================================================================
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ============================================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# ----------------------------------------------------------------------------
# STATIC_ROOT: destino de `collectstatic` (Nginx la sirve en EC2).
# STATICFILES_DIRS: carpeta `static/` para CSS/JS propios.
# MEDIA_ROOT: archivos subidos (exámenes, fotos de mascotas, etc.).
# ============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================================
# AUTENTICACIÓN — LOGIN / LOGOUT
# ============================================================================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# ============================================================================
# DJANGO REST FRAMEWORK
# ----------------------------------------------------------------------------
# Autenticación por sesión + Basic. Permiso por defecto: autenticado.
# ============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# ============================================================================
# CLAVE PRIMARIA POR DEFECTO
# ============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# SEGURIDAD DE SESIONES
# ----------------------------------------------------------------------------
# En un sistema clínico, es crucial que las sesiones expiren por inactividad
# para proteger la privacidad de las fichas médicas.
# SESSION_COOKIE_AGE: Tiempo de vida de la cookie de sesión en segundos.
#   3600 = 60 minutos. (Puedes poner 1800 para 30 minutos).
# SESSION_EXPIRE_AT_BROWSER_CLOSE: Si es True, la sesión muere al cerrar el
#   navegador. Lo dejamos en False para que el usuario no pierda el trabajo si
#   cierra la pestaña por error, pero la inactividad lo sacará.
# SESSION_SAVE_EVERY_REQUEST: Si es True, el contador de expiración se reinicia
#   cada vez que el usuario hace clic o recarga una página. Esto es ideal para
#   medir "inactividad" real.
# ============================================================================
SESSION_COOKIE_AGE = 3600  # 60 minutos
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True