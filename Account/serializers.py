from rest_framework import serializers
from .models import User
from Tasks.models import Task
from Tasks.serializers import TaskSerializer

class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'max_length': 20},
            'email': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
        }

    def get_tasks(self, obj):
        result = obj.tasks.all()
        serializer_data = TaskSerializer(instance=result, many=True)
        return serializer_data.data

    def create(self, validated_data):
        validated_data['is_active'] = True
        return super().create(validated_data)