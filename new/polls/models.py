from django.db import models
from django.conf import settings

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Question no {}').format(self.id)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 300)
    votes = models.IntegerField(default = 0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Choice for question {}').format(self.question.id)

class Comment(models.Model):
    comment_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date commented')
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Comment of Question{}').format(self.question.id)
