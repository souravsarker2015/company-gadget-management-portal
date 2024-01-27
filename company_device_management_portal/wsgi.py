import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_device_management_portal.settings')

application = get_wsgi_application()
