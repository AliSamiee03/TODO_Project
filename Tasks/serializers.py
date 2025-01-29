from rest_framework import serializers
from .models import Task
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('creator', 'created_at', 'updated_at')


    def validate_due_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("The due date cannot be in the past.")