"""
Django settings for API project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import decouple
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(l2%=61ue!xphtji$-v-%xmua2w*2s4zbtl$#o!327b@n24q+-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 3
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework_swagger', # documentation module

    'BillSays',

    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'django_dropbox',

    #tool for code generating
    'drf_generators',

    #tool for S3 Amazon storage access
    'drf_to_s3',
    'storages',



]

REST_USE_JWT = True

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': False  # Default: False
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_LOGOUT_ON_GET = True

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        #'SCOPE': ['email', 'publish_stream'],
        'SCOPE': ['email', 'publish_actions'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BillSays.urls'

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

WSGI_APPLICATION = 'API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':
            #'Dota',
            'dcm6b473plgp9o',
        'USER':
            #'lucas63',
            'hgtxjigpasgdxu',
        'PASSWORD':
            #'1234',
            'UAUdl7cbfwf-HhyWO_NSiCd7Co',
        'HOST':
            #'localhost',
            'ec2-54-243-223-22.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Documentation settings

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/docs/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '(l2%=61ue!xphtji$-v-%xmua2w*2s4zbtl$#o!327b@n24q+-', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}



# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/Checks/'
MEDIA_ROOT=os.path.join(BASE_DIR,'Checks/')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#For email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'malenovskiy2463@gmail.com'

#Must generate specific password for your app in [gmail settings][1]
EMAIL_HOST_PASSWORD = 'KOBE2463'
EMAIL_PORT = 587

#This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


#Facebook

SOCIAL_AUTH_FACEBOOK_KEY = '1736562713290446|bbkqpUqNL8BH39SOw1Zw_rf6j2U'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b46acee6fe22458c4a1c2087d1c185bb'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

#dropbox

DROPBOX_CONSUMER_KEY = 'z503ozdn1jw6mpr'
DROPBOX_CONSUMER_SECRET = '2pta13cspew835w'
DROPBOX_ACCESS_TOKEN = 'i53lqk0rzcjtqi82'
DROPBOX_ACCESS_TOKEN_SECRET = 'd4zkw8tne7s616j'

#Amazon S3
AWS_STORAGE_BUCKET_NAME = 'billsays'
AWS_ACCESS_KEY_ID = 'AKIAIUXCCBDDCMATLHXA'
AWS_SECRET_ACCESS_KEY = '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'

AWS_S3_CUSTOM_DOMAIN = 'billsays.s3.amazonaws.com'



DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATICFILES_LOCATION = 'static'
#STATIC_URL = "https://%billsays.s3.amazonaws.com/"
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MEDIAFILES_LOCATION = 'Checks'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'