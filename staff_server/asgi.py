import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staff_server.settings')


from django.core.asgi import get_asgi_application
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from django.core.cache import cache
cache.clear()



from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from .routing import url_patterns as wsPaths
from utils.auth import TokenAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                wsPaths
            )
        )
    )
    
})