import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from sale.routing import urlrouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sale.settings')

application = get_asgi_application()
