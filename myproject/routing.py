# from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.urls import path
# from chat import consumers
# import chat.routing
# from channels.http import AsgiHandler
# from django.core.asgi import get_asgi_application

# application = ProtocolTypeRouter(
#     {
#         "http": AsgiHandler(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
#         ),
#     }
# )