# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat import consumers
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
