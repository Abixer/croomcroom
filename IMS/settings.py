"""
Django settings for IMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

ENVIRONMENT = "PRODUCTION"
#ENVIRONMENT = "STAGING"
#ENVIRONMENT = "DEV"



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z@c9_l9pehzy@67r7@2=3+ryg3xr!7q@))=7l#(5xr_)mt#$f0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',
	'preview',
	'allauth',
    'allauth.account',
    'allauth.socialaccount',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (    
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",  
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'IMS.urls'

WSGI_APPLICATION = 'IMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}

if ENVIRONMENT == "PRODUCTION":
	import dj_database_url
	DATABASES['default'] =  dj_database_url.config(default=os.environ["HEROKU_POSTGRESQL_WHITE_URL"])
	DEFAULT_FROM_EMAIL = 'postmaster@croomer.com'
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = 'smtp.mailgun.org'
	EMAIL_PORT = 25
	EMAIL_HOST_USER = 'postmaster@croomer.com'
	EMAIL_HOST_PASSWORD = '0a-afhbk6xi2'
	EMAIL_USE_TLS = False
elif ENVIRONMENT == "STAGING":
	import dj_database_url
	DATABASES['default'] =  dj_database_url.config(default=os.environ["HEROKU_POSTGRESQL_RED_URL"])
	DEFAULT_FROM_EMAIL = 'postmaster@croomer.com'
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = 'smtp.mailgun.org'
	EMAIL_PORT = 25
	EMAIL_HOST_USER = 'postmaster@croomer.com'
	EMAIL_HOST_PASSWORD = '0a-afhbk6xi2'
	EMAIL_USE_TLS = False
elif ENVIRONMENT == "DEV":
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'croomerDB',                      
			'USER': 'croomerUser',
			'PASSWORD': 'croomer',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}
	DEFAULT_FROM_EMAIL = 'postmaster@croomer.com'
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1




# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SETTINGS ALLAUTH
LOGIN_REDIRECT_URL = '/demo/dashboard'
# Specifies the login method to use – whether the user logs in by entering his username, e-mail address, or either one of both.
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# Determines whether or not an e-mail address is automatically confirmed by a mere GET request.
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
# The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/demo/dashboard'
# The user is required to hand over an e-mail address when signing up.
ACCOUNT_EMAIL_REQUIRED = True
# Determines the e-mail verification method during signup – choose one of “mandatory”, “optional”, or “none”. When set to “mandatory” the user is blocked from logging in until the email address is verified. Choose “optional” or “none” to allow logins with an unverified e-mail address. In case of “optional”, the e-mail verification mail is still sent, whereas in case of “none” no e-mail verification mails are sent.
ACCOUNT_EMAIL_VERIFICATION = 'none'
# Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.
ACCOUNT_EMAIL_SUBJECT_PREFIX ='[croomer.com]'
# Determines whether or not the user is automatically logged out by a mere GET request. See documentation for the LogoutView for details.
ACCOUNT_LOGOUT_ON_GET = True
# The URL (or URL name) to return to after the user logs out. This is the counterpart to Django’s LOGIN_REDIRECT_URL.
ACCOUNT_LOGOUT_REDIRECT_URL = '/demo'
#A  string pointing to a custom form class (e.g. ‘myapp.forms.SignupForm’) that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date). 
ACCOUNT_SIGNUP_FORM_CLASS = 'demo.forms.SignupForm'
# An integer specifying the minimum allowed length of a username.
ACCOUNT_USERNAME_MIN_LENGTH = 3
# An integer specifying the minimum password length.
ACCOUNT_PASSWORD_MIN_LENGTH = 5

AUTH_PROFILE_MODULE = 'demo.UserProfile'
LOGIN_URL = '/demo/'
