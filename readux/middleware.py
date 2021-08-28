from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key):
    # If you are using normal token based authentication
    try:
        token = Token.objects.get(key=token_key)
        print('Token: ', token)
        return token.user
    except Token.DoesNotExist:
        raise Http404



class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
            print("Key",token_key)
        except ValueError:
            token_key = None
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)