"""
Django settings for data_donation project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/bucket/login/'

SESSION_COOKIE_AGE = 8640000

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0300u%!t9%z!si5j&q@95@^_$8qda+$mrii*751b7v#ai2vzv-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'channels_redis',
    #'causes',
    'about',
    'pages',
    'environ',
    'bucket',
    'bucket_view',
    'plot_test',
    'atm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
]

ROOT_URLCONF = 'data_donation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["data_donation/templates/"],
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

WSGI_APPLICATION = 'data_donation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# File Uploads
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "%d %m %Y"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR /"static"]

# AUTHLIB CLIENTS
AUTHLIB_OAUTH_CLIENTS = {
    'google': {
        'client_id': env('GOOGLE_CLIENT_ID'),
        'client_secret': env('GOOGLE_CLIENT_SECRET'),
    },
    'bucket': {
        'client_id': env('DATA_DONATION_CLIENT_ID'),
        'client_secret': None,
    }
}

AUTH_USER_MODEL = "bucket.BucketUser" # Default model for authentication

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'bucket.auth.BucketAuthenticationBackend',
)

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,

    'formatters' : {
        'timestamp' : {
            'format' : '{levelname} {asctime} {message}',
            'style' : '{',
        },
    },

    'handlers' : {
        'console' : {
            'class' : 'logging.StreamHandler',
            'level' : 'INFO',
            'formatter': 'timestamp',
        },
        'file' : {
            'class' : 'logging.FileHandler',
            'filename' : 'data_donation/logs/log_file.log',
            'level' : 'INFO',
            'formatter': 'timestamp',
        }
    },
    'root' : {
      'handlers' : ['console', 'file'],
      'level' : 'INFO'
    },

    'loggers' : {
        'django' :{
            'handlers' : ['console', 'file'],
            'level' : 'ERROR',
            'propagate' : False,
        },
        'data_donation_logs' : {
            'handlers' : ['console', 'file'],
            'level' : 'INFO',
            'propagate': False,
        }
    },
}

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Amsterdam'

# PLOTLY DASH
X_FRAME_OPTIONS = 'SAMEORIGIN'
CRISPY_TEMPLATE_PACK = 'boostrap4'

ASGI_APPLICATION = 'data_donation.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
        },
    },
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
]

PLOTLY_COMPONENTS = [

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    'dpd_components',
]