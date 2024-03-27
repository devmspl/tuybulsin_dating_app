"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
settings.configure()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
     "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
})


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })



