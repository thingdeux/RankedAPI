import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
SECRET_KEY = "962)!uu2&-s9t=^t7hh^0lk-l9mh$@-pss4#a0ru#(laiq+j%x"
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = "DENY"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'RankedDev',
        'USER': 'rankeddbadmin',
        'PASSWORD': '40hff!9939fhhbvc',
        'HOST': 'ranked-dev-db.cgafuwikv4jj.us-west-2.rds.amazonaws.com',
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'
STATICFILES_DIRS = [
]