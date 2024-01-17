from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import AuthTokenSerializer


class CreateToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES