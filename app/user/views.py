from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthenticateTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthenticateTokenSerializer
    # specify the renderer class since obtain_auth_token view by default explicitly uses JSON requests and responses.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


"""
Note that the URL part of the pattern can be whatever you want to use.

The obtain_auth_token view will return a JSON response when valid username and password fields 
are POSTed to the view using form data or JSON:

{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
Note that the default obtain_auth_token view explicitly uses JSON requests and responses, 
rather than using default renderer and parser classes in your settings.

By default, there are no permissions or throttling applied to the obtain_auth_token view. If you do wish to apply
to throttle you'll need to override the view class, and include them using the throttle_classes attribute.

If you need a customized version of the obtain_auth_token view, you can do so by subclassing the 
ObtainAuthToken view class, and using that in your url conf instead.

For example, you may return additional user information beyond the token value:

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
And in your urls.py:

urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
"""
