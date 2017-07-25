import os
import platform
from urllib import request

ALLOWED_HOSTS = ['api.goranked.com', '54.245.67.189']

# AWS ELB Health Checker uses the instances local IP to perform health checks. Django will raise suspicious
# Exception if the ip is not added to the allowed_hosts.  Using the AWS instance metadata to pull the
# hosts ip and append it to ALLOWED on startup.
# More Info: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html

try:
    response = request.urlopen('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01)
    EC2_IP = response.read().decode('utf-8')
    ALLOWED_HOSTS.append(EC2_IP)
except Exception:
    pass



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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://rankeddemo.eq7ccp.ng.0001.usw2.cache.amazonaws.com:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'
STATICFILES_DIRS = [
]
