from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthenticateTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Creates a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthenticateTokenSerializer
    # specify the renderer class since obtain_auth_token view by default explicitly uses JSON requests and responses.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manages the authenticated user
    Allows only GET, PUT, & PATCH http methods
    """
    serializer_class = UserSerializer
    # takes the authenticated user and assign the user to request
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authentication user"""
        return self.request.user
