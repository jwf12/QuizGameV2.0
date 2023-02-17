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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     preguntas_respuestas = {}

    #     for quiz in context['object_list']:
    #         preguntas = quiz.question_set.all()
    #         for pregunta in preguntas:
    #             respuestas = pregunta.answer_set.all()
    #             preguntas_respuestas[pregunta] = respuestas

    #     context['preguntas_respuestas'] = preguntas_respuestas
    #     return context


class QuestionView(LoginRequiredMixin, generic.ListView):
    model = Question
    template_name = 'questions.html'
    context_object_name = 'preguntas'

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        quiz = get_object_or_404(Quiz, pk = quiz_id)
        return Question.objects.filter(quiz = quiz)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preguntas_respuestas = {}

        for pregunta in context['preguntas']:
            respuestas = pregunta.answer_set.all()
            preguntas_respuestas[pregunta] = respuestas
            
        context['preguntas_respuestas'] = preguntas_respuestas
        return context






class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('quiz:login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Tu cuenta ha sido creada! Por favor inicia sesión.')
        return response
