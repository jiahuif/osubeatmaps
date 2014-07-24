
from osubeatmaps.settings import *

INSTALLED_APPS = tuple(set(list(INSTALLED_APPS) + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]))

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'osubeatmaps.urls_admin'

WSGI_APPLICATION = 'osubeatmaps.wsgi_admin.application'

SESSION_ENGINE = "django.contrib.sessions.backends.file"