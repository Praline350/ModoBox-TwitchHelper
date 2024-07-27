import os
import django


print("Définir DJANGO_SETTINGS_MODULE")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
print("DJANGO_SETTINGS_MODULE est défini : ", os.environ.get('DJANGO_SETTINGS_MODULE'))

django.setup()
print("Django setup completed")
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from whitenoise import WhiteNoise
from django.core.handlers.asgi import ASGIHandler
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
import chat.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(get_asgi_application()),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
print("ASGI application configurée")