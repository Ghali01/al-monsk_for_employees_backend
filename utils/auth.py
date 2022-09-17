from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(key):
    try:
        return Token.objects.get(key=key).user
    except (Token.DoesNotExist,KeyError):
        return AnonymousUser()
  
class TokenAuthMiddleware:

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        if b'token' in dict(scope['headers']): 
            token=str(dict(scope['headers'])[b'token'])[2:-1]
            scope['user'] = await get_user(token)

        return await self.app(scope, receive, send)