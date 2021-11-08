from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.settings import api_settings

from users.tasks import hello
from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Endpoint for user creation"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    """Manage tha authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        res = hello.delay()
        return self.request.user
