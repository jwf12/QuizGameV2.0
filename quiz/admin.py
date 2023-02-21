from django.contrib import admin
from .models import Question, Quiz, Answer,UserProgress


class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        'update_at',
    )


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'quiz',
        'text',
    )


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'text',
        'is_correct',
    )




admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserProgress)
