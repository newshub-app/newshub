"""
Django settings for newshub project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#
# Django settings
# https://docs.djangoproject.com/en/5.0/ref/settings/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "NEWSHUB_SECRET_KEY",
    "django-insecure-9iea-5+mfz2&xofs$$1kqxb79uj)gj9^el1bk4lgiq%_6$itwg",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("NEWSHUB_DEBUG", "false").lower() == "true"
TESTING = "test" in sys.argv

ALLOWED_HOSTS = os.environ.get(
    "NEWSHUB_ALLOWED_HOSTS", "127.0.0.1,.localhost,[::1]"
).split(",")

INTERNAL_IPS = os.environ.get(
    "NEWSHUB_INTERNAL_IPS", "127.0.0.1,.localhost,[::1]"
).split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    # "rest_framework",
    # "rest_framework_simplejwt",
    "django_filters",
    "django_bootstrap5",
    "authnz.apps.AuthnzConfig",
    "news.apps.NewsConfig",
    # "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "newshub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "news.context_processors.new_link_form",
            ],
        },
    },
]

WSGI_APPLICATION = "newshub.wsgi.application"

#
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NEWSHUB_DB_NAME", "newshub"),
        "USER": os.environ.get("NEWSHUB_DB_USER", "newshub"),
        "PASSWORD": os.environ.get("NEWSHUB_DB_PASSWORD", "newshub"),
        "HOST": os.environ.get("NEWSHUB_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("NEWSHUB_DB_PORT", "5432"),
    }
}

#
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

#
# Authentication
# https://docs.djangoproject.com/en/5.0/topics/auth/default/

AUTH_USER_MODEL = "authnz.User"

LOGIN_URL = "authnz:login"

LOGIN_REDIRECT_URL = "news:index"

LOGOUT_REDIRECT_URL = "news:index"

PASSWORD_RESET_TIMEOUT = 3600  # password reset links expire after 1 hour

#
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

#
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

#
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#
# CORS
# https://github.com/adamchainz/django-cors-headers?tab=readme-ov-file#configuration

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8000"]

#
# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "URL_FIELD_NAME": "resource_url",
}

#
# Django debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "mail_panel.panels.MailToolbarPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED": True,
    "DISABLE_PANELS": [
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ],
}

DEBUG_TOOLBAR_APPS = [
    "debug_toolbar",
    "mail_panel",
]

#
# Django debugging settings

if DEBUG and not TESTING:
    INSTALLED_APPS += DEBUG_TOOLBAR_APPS
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
    EMAIL_BACKEND = "mail_panel.backend.MailToolbarBackend"
    CORS_ALLOW_ALL_ORIGINS = True
