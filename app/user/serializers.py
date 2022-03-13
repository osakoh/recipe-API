from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

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

    def update(self, instance, validated_data):
        """
        Updates a users password
        instance: model instance
        validated_data: the fields ('email', 'password', 'name')
        """
        # gets the password and removes it from the validated dictionary
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthenticateTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField(
        error_messages={
            "null": _("Email is a required field cannot be null."),
            "blank": _("Email is a required field, cannot be blank."),
        },
    )  # creates a new field
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,  # stop DRF from automatically trimming whitespace in password
        error_messages={
            "null": _("Password is a required field."),
            "blank": _("Password is a required field."),
        },
    )

    def validate(self, attrs):
        """ Validate and authenticate the user"""
        # retrieve email from the attributes i.e. fields in the serializer
        email = attrs.get('email')
        # retrieve password from the attributes i.e. fields in the serializer
        password = attrs.get('password')

        # returns a User object if the given credentials are valid. i.e. user: a@a.com self.context: {'request':
        # <rest_framework.request.Request: POST '/api/user/token/'>, 'format': None,
        # 'view': <user.views.CreateTokenView object at someRandomCharsRepMemoryObject>}
        user = authenticate(
            request=self.context.get('request'),
            username=email,  # using the users's email as username since the user object has been customised
            password=password
        )

        # authentication fails
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # DRF passes the error as a 400 response(status code, bad response)
            raise serializers.ValidationError(msg, code='authentication')

        # successful validation, return the attrs(values at the end) when overriding the validate function
        attrs['user'] = user
        return attrs
