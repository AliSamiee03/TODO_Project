from .serializers import TaskSerializer
from .models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from permissions import IsOwnerTaskOrAdmin

class ListTasks(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer_data = TaskSerializer(instance=tasks, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


class DetailTask(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        serializer_data = TaskSerializer(instance=task)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

class CreateTask(APIView):

    def post(self, request):
        serializer_data = TaskSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTask(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        serializer_data = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTask(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)