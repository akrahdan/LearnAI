from readux.middleware import TokenAuthMiddleware
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chats.consumers import ChatConsumer, ChatNewConsumer
application = ProtocolTypeRouter({ 
    # Websocket chat handler
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                [
                    url(r"ws/compose/(?P<username>[\w.@+-]+)/$", ChatNewConsumer(), name='compose'),
                    url(r"ws/messages/(?P<room_id>[\w.@+-]+)/$", ChatConsumer.as_asgi(), name='chat')
                ]
            )
        ),
    )
})