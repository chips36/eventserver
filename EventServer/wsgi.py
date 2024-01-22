"""
WSGI config for EventServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

# add the hellodjango project path into the sys.path
sys.path.append('C:/01.SRC/EventServer')

# add the virtualenv site-packages path to the sys.path
sys.path.append('C:/01.SRC/EventServer/venv/Lib/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventServer.settings')


application = get_wsgi_application()
