from .serializers import TaskSerializer
from .models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from permissions import IsOwnerTaskOrAdmin
from django.utils.timezone import now
from django.utils.dateparse import parse_date


class ShowAllTasksView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        tasks = Task.objects.all()

        due_date = request.query_params.get('due_date')
        created_at = request.query_params.get('created_at')

        if due_date:
            due_date = parse_date(due_date)
            if due_date:
                tasks = tasks.filter(due_date=due_date)

        if created_at:
            created_at = parse_date(created_at)
            if created_at:
                tasks = tasks.filter(created_at__date=created_at)

        serializer = TaskSerializer(instance=True, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListTasks(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def get(self, request):
        tasks = Task.objects.filter(creator=request.user)


        due_date = request.query_params.get('due_date')
        created_at = request.query_params.get('created_at')

        if due_date == 'true':
            tasks = tasks.order_by('due_date')

        if created_at == 'true':
            tasks = tasks.order_by('created_at')

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
            serializer_data.save(creator=request.user)
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTask(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        serializer_data = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save(updated_at=now())
            return Response(serializer_data.data, status=status.HTTP_200_OK)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTask(APIView):
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)