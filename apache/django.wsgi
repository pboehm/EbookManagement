import os, sys
sys.path.append('/usr/local/django')
sys.path.append('/usr/local/django/EbookManagement/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'EbookManagement.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

