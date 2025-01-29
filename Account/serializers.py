from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 20},
            'email': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
        }
