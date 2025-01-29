from django.urls import path
from . import views

urlpatterns = [
    path('list_tasks/', views.ListTasks.as_view(), name='list_tasks'),
    path('detail_task/<int:pk>/', views.DetailTask.as_view(), name='detail_task'),
    path('create_task/', views.CreateTask.as_view(), name='create_task'),
    path('update_task/<int:pk>/', views.UpdateTask.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', views.DeleteTask.as_view(), name='delete_task'),
    path('show_all_tasks/', views.ShowAllTasksView.as_view(), name='show_all_tasks'),
]