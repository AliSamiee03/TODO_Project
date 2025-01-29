from django.urls import path
from . import views
urlpatterns = [
    path('list_users/', views.ListUsersView.as_view(), name='list_users'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('update_user/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
]