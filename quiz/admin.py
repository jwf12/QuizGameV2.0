from django.contrib import admin
from .models import Question, Quiz


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


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)

