from .serializers import TaskSerializer
from .models import Task
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from permissions import IsOwnerTaskOrAdmin
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.db.models import Q

class ShowAllTasksView(APIView):
    """
    Show tasks of all users
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = TaskSerializer
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
    """
    Show all the tasks of the logged in user
    """
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]
    serializer_class = TaskSerializer

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
    """
    Show details of a task
    """
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]
    serializer_class = TaskSerializer

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        serializer_data = TaskSerializer(instance=task)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

class CreateTask(APIView):
    """
    Create a new task
    """
    serializer_class = TaskSerializer

    def post(self, request):
        serializer_data = TaskSerializer(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save(creator=request.user)
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTask(APIView):
    """
    Update a task
    """
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]
    serializer_class = TaskSerializer

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        serializer_data = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save(updated_at=now())
            return Response(serializer_data.data, status=status.HTTP_200_OK)

        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTask(APIView):
    """
    Delete a task
    """
    permission_classes = [IsAuthenticated, IsOwnerTaskOrAdmin]

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchTaskView(APIView):
    """
    Search task by title or description
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request):
        searched_word = request.query_params.get('search')
        print(searched_word)
        if searched_word:
            tasks = Task.objects.filter(
                Q(title__icontains=searched_word) | Q(description__icontains=searched_word), creator=request.user
            )
            self.check_object_permissions(request, tasks)
            serializer_data = TaskSerializer(tasks, many=True)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response({"detail": "Query parameter 'search' is required."}, status=status.HTTP_400_BAD_REQUEST)