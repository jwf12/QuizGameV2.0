from django.shortcuts import render
from .models import Quiz, Question, Answer, UserProgress
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
# Create your views here.


# def home(request):
#     return render(request, 'index.html')


class Home(LoginRequiredMixin, generic.ListView):
    model = Quiz
    template_name = 'index.html'
    context_object_name = 'categorias'
    login_url = 'quiz:login'


class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('quiz:login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Tu cuenta ha sido creada! Por favor inicia sesión.')
        return response


