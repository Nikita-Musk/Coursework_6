from django.urls import path

from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView, email_verification, toggle_activity, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]