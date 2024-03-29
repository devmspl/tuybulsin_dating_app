# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
