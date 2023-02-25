from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Home, SingUpView, QuestionView, CustomLoginView,ScoreView


app_name = 'quiz'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('register/', SingUpView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'login.html'), name = 'logout'),
    path('questions/<int:quiz_id>/', QuestionView.as_view(), name = 'question_list'),
    path('score/', ScoreView.as_view(), name='score'),
    path('', Home.as_view(), name = 'home'),
]
