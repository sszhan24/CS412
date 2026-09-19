"""
WSGI config for temp_name project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/home/s/sszhan24/webapps/django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')

application = get_wsgi_application()
