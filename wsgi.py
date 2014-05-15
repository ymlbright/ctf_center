import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
#father dir
sys.path.append('/var/www/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ctfsystem.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
