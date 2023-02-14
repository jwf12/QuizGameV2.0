from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'quiz'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html')),
    path('register/', auth_views.LoginView.as_view(template_name = 'register.html'), name='register'),

]
