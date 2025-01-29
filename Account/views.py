from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from permissions import IsOwnerOrAdmin
class CreateUserView(APIView):
    """
    Create a new user
    """
    serializer_class = UserSerializer

    def post(self, request):
        serializer_data = UserSerializer(data=request.data)
        if serializer_data.is_valid():
            user = serializer_data.save()
            user.set_password(serializer_data.validated_data['password'])
            user.save()
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersView(APIView):
    """
    View to list all users
    """
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer_data = UserSerializer(instance=users, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

class DetailUserView(APIView):
    """
    View a user's information
    """
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        self.check_object_permissions(request, user)
        serializer_data = UserSerializer(instance=user)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

class UpdateUserView(APIView):
    """
    Updates the user
    """

    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    serializer_class = UserSerializer

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        self.check_object_permissions(request, user)
        serializer_data = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    """
    Delete user
    """
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
