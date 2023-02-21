from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
        


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    complated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.score
