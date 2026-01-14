import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w6m$@irrvzwxl7+(^m7v3x39jz@^5q6@t8121z5cegm_hevjt0'

# SECURITY WARNING: don't run with debug turned on in production!
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
    
    # Third-party apps
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',  # optional, for Swagger UI assets
    
    # Local apps
    'api',
    'generator',
    
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

ROOT_URLCONF = 'qrtist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'qrtist.wsgi.application'


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


CSRF_COOKIE_HTTPONLY = False  # Allows JavaScript to read CSRF token
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Create these directories
os.makedirs(BASE_DIR / 'static', exist_ok=True)
os.makedirs(BASE_DIR / 'media/qr_codes', exist_ok=True)
os.makedirs(BASE_DIR / 'media/uploads', exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}



# Spectacular settings
SPECTACULAR_SETTINGS =  {
    'TITLE': 'QRtist API',
    'DESCRIPTION': 'API documentation for QRtist application',
    'VERSION': '1.0.0',
    'TERMS_OF_SERVICE': 'https://www.google.com/policies/terms/',
    'CONTACT': {'email': 'maruf.bshs@gmail.com'},
    'LICENSE': {'name': 'BSD License'},
    'SERVE_INCLUDE_SCHEMA': False,  # optional: hides raw schema in UI
}



# Jazzmin settings

JAZZMIN_SETTINGS = {
    "site_title": "QRtist Admin",
    "site_header": "QRtist",
    "site_brand": "QRtist",
    "site_logo": "images/logo.png",  # optional, we can skip for now
    "welcome_sign": "Welcome to the QRtist Admin Panel",
    "copyright": "QRtist © 2026",

    # top-right user menu
    "user_avatar": None,

    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # Your models
        "paper.Paper": "fas fa-book",
        "paper.UserUpload": "fas fa-upload",
    },

    # Side menu ordering
    "default_icon_parents": "fas fa-chevron-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lux",   # clean light Bootstrap theme
    "dark_mode_theme": "darkly",  
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,

    "brand_color": "primary",
    "accent": "primary",
    "navbar": "navbar-dark bg-primary",
    "no_navbar_border": False,
}