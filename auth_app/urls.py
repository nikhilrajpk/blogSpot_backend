from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserDetailView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/me/', CurrentUserView.as_view(), name='current_user'),
]