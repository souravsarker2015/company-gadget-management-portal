import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_gadget_management_portal')

application = get_asgi_application()
