from django.shortcuts import render
from .models import Quiz, Question, Answer, UserProgress
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
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


# class QuestionView(LoginRequiredMixin, generic.ListView):
#     model = Question
#     template_name = 'questions.html'
#     context_object_name = 'preguntas'

#     def get_queryset(self):
#         quiz_id = self.kwargs.get('quiz_id')
#         quiz = get_object_or_404(Quiz, pk = quiz_id)
#         return Question.objects.filter(quiz = quiz)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         preguntas_respuestas = {}

#         for pregunta in context['preguntas']:
#             respuestas = pregunta.answer_set.all()
#             preguntas_respuestas[pregunta] = respuestas
            
#         context['preguntas_respuestas'] = preguntas_respuestas
#         return context


class QuestionView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'questions.html'

    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        session = request.session

        if 'current_question' not in session:
            # Si no hay una pregunta actual en la sesión, se empieza con la primera pregunta del quiz
            current_question = quiz.question_set.first().id
            session['current_question'] = current_question
            session['correct_answers'] = 0
        else:
            current_question = session['current_question']

        question = get_object_or_404(Question, pk=current_question)


        answers = question.answer_set.all()

        return render(request, self.template_name, {
            'quiz': quiz,
            'question': question,
            'answers': answers
        })

    def post(self, request, *args, **kwargs):
        quiz_id = kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        session = request.session

        # Se obtiene la respuesta seleccionada por el usuario
        selected_answer_id = request.POST.get('answer')

        if selected_answer_id:
            selected_answer = get_object_or_404(Answer, pk=selected_answer_id)
            if selected_answer.is_correct:
                # Si la respuesta es correcta, se incrementa el número de respuestas correctas
                session['correct_answers'] += 1

        # Se obtiene la siguiente pregunta del quiz
        current_question = session['current_question']
        next_question = quiz.question_set.filter(id__gt=current_question).first()
        
        if next_question:
            # Si hay una siguiente pregunta, se actualiza la pregunta actual en la sesión
            session['current_question'] = next_question.id
        else:
            # Si no hay una siguiente pregunta, se ha completado el quiz y se muestra el resultado
            score = session['correct_answers']
            total_questions = quiz.question_set.count()
            user = request.user
            complated_at = timezone.now().date()
            # Se crea una istancia de userprogress para almacenarlo en base de datos.
            user_progress = UserProgress.objects.create(user=user, quiz=quiz, score=score,complated_at=complated_at)

            return render(request, 'quiz_result.html', {
                'quiz': quiz,
                'correct_answers': session['correct_answers'],
                'total_questions': quiz.question_set.count()
            })

        # Se renderiza la plantilla de la siguiente pregunta
        question = next_question
        answers = question.answer_set.all()
        return render(request, self.template_name, {
            'quiz': quiz,
            'question': question,
            'answers': answers
        })


class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('quiz:login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Tu cuenta ha sido creada! Por favor inicia sesión.')
        return response