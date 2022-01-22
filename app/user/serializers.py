from django.contrib.auth import get_user_model
# from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # extra settings: ensures password is not returned to the response data & it contains at least 5 characters
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)
