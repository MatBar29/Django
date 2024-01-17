from rest_framework import serializers
from django.contrib.auth import authenticate

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=("Username"))
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs