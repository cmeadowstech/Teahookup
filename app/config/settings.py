"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    DJANGO_SECRET_KEY=(
        str,
        "django-insecure-7g7e&!bdy!f7i+2roz@c&rrabdpq#0r)pc6fohmy$j-66y_%v_",
    )
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECRET_KEY = 'django-insecure-7g7e&!bdy!f7i+2roz@c&rrabdpq#0r)pc6fohmy$j-66y_%v_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://*.tealist.fly.dev", "https://*teahookup.com"]

INTERNAL_IPS = [
    env.str("DEBUG_IP", default=""),
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Django whitenoise
    "django.contrib.staticfiles",
    "django_extensions",  # Django Extensions for runscript
    "django_filters",  # Django Filters
    "django_htmx",  # HTMX middleware
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # allauth Google
    "debug_toolbar",  # Django debug toolbar
    "request",  # django-request
    "django_comments_xtd",  # django_comments_xtd
    "django_comments",  # django_comments_xtd
    "matomo",  # django-matomo
    "tailwind",  # django-tailwind
    "django_browser_reload",  # django-tailwind[reload]
    "tealist",
    "theme",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "request.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Django debug toolbar
    "django_browser_reload.middleware.BrowserReloadMiddleware",  # django-tailwind[reload]
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    "default": env.db(default=""),
    # read os.environ['SQLITE_URL']
    "extra": env.db_url("SQLITE_URL", default="sqlite:////tmp/my-tmp-sqlite.db"),
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# django_storages auth


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files

try:
    AZURE_ACCOUNT_NAME = "thstorage981357"
    AZURE_CONTAINER = "files"
    AZURE_ACCOUNT_KEY = env("STORAGE_ACCOUNT_KEY")
    AZURE_OVERWRITE_FILES = "True"

    INSTALLED_APPS.append("storages")
    DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
except:
    pass

MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Directory where uploaded media is saved.
MEDIA_URL = "/media/"  # Public URL at the browser

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# allauth settings

if not DEBUG:
    SITE_ID = 5
else:
    SITE_ID = 3

REQUEST_BASE_URL = "https://teahookup.com/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY", default="")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "mail@teahookup.com"


# Miscellaneous

# Logging

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "formatters": {
        "superverbose": {
            "format": "%(levelname)s %(asctime)s %(module)s:%(lineno)d %(process)d %(thread)d %(message)s"
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s:%(lineno)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "superverbose",
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file"],
        }
    },
}

# django_comments_xtd settings

COMMENTS_APP = "django_comments_xtd"

COMMENTS_XTD_SALT = (
    b"Timendi causa est nescire. " b"Aequam memento rebus in arduis servare mentem."
)

COMMENTS_XTD_MAX_THREAD_LEVEL = 2  # default is 0
COMMENTS_XTD_LIST_ORDER = ("-thread_id", "order")  # default is ('thread_id', 'order')

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "default": {
        "allow_flagging": True,
        "allow_feedback": True,
        "show_feedback": True,
        "who_can_post": "users",
    }
}

# django-matomo

MATOMO_SITE_ID = 2
MATOMO_URL = "https://analytics.teahookup.com/"

# Glitchtip

sentry_sdk.init(
    dsn="https://77fa51e202684ed4a5310e0d20d2a7b4@glitchtip.teahookup.com/1",
    integrations=[DjangoIntegration()],
    auto_session_tracking=False,
    traces_sample_rate=0,
)

# Cache

CACHE_TTL = 60 * 60
CACHES = {
    "default": env.cache(
        default="rediscache://:@:6379/1/?key_prefix=teahookup"
    )  # default = 'CACHE_URL' environmennt variable
    # 'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache',}
}

# Tailwind

TAILWIND_APP_NAME = "theme"
