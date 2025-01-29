from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('list_users/', views.ListUsersView.as_view(), name='list_users'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('update_user/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path('detail_user/<int:pk>/', views.DetailUserView.as_view(), name='detail_user'),
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODIyODUyMywiaWF0IjoxNzM4MTQyMTIzLCJqdGkiOiJkNWZmNTkxNjMyMjQ0MzVlOTcyNGMyM2Q0ODNiZWZkNyIsInVzZXJfaWQiOjF9.x82T-I5fAXpxrO-G_-ZYbsVN2biyvBjDfeL8uAIx0ms",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MTQyNDIzLCJpYXQiOjE3MzgxNDIxMjMsImp0aSI6ImFjOGQxYWJmOWJlZjRhZWY5ODVhMWQ4YzczNmQ1NTFlIiwidXNlcl9pZCI6MX0.t7mOlpa8h1JidcBXE1ORYwB4L-G8RFgRStCQhDlsqQc"
# }