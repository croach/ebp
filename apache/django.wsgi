import os
import sys

DJANGO_PROJECTS_DIR = '/home/croach/django'
PROJECT_DIR = os.path.join(DJANGO_PROJECTS_DIR, 'ebp')

sys.path.append(DJANGO_PROJECTS_DIR)
sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ebp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
