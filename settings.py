# -*- coding: utf-8 -*-
# Django settings for EbookManagement project.
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'ebooks.db'), 
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Pfad zu den Ebooks
EBOOK_PATH = '/var/ebooks/'
if DEBUG == True:
    EBOOK_PATH = '/home/philipp/Desktop/Ebooks'

####
# Moeglichkeiten fuer Ebooks
CHOICES_FOR_EBOOKS = [
        ('', '-------------'),
        ('info', 'Informationen anzeigen'),
        ('move', 'Verschieben'),
        ('delete', 'Löschen'),
        ('push2kindle', 'An Kindle versenden'),
    ]

####
# Existierende Icons laden
EXISTING_FILE_ICONS = []
for icon in os.listdir(os.path.join(PROJECT_ROOT, 'static', 'fileicons')):
    EXISTING_FILE_ICONS.append(icon.split('.')[0])

###
# Statische Daten
MEDIA_ROOT = EBOOK_PATH
MEDIA_URL = '/media/'

STATIC_ROOT = '' 
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '*j$7$y5h)1di3s#l*+wj6+ji1gtms%$2g2lh=)pc&o%+w2$lql'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'EbookManagement.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'EbookManagement.ebooks',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
