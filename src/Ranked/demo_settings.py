import os
import platform


ALLOWED_HOSTS = ['demo.goranked.com']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG = False
SECRET_KEY = "962)!uu3455567^t7hh^0lk-l9mh$@-pss4#a0ru#(laiq+j%x"
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = "DENY"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'RankedDemo',
        'USER': 'rankeddbadmin',
        'PASSWORD': '40hff!9939fhhbvc',
        'HOST': 'rankeddemodb.cgafuwikv4jj.us-west-2.rds.amazonaws.com',
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'
STATICFILES_DIRS = [
]
