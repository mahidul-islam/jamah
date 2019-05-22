import uuid
from django.db import models
from django.conf import settings
from event.models import Event
from django.db.models.signals import post_save
from django.utils import timezone


class Question(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published', default = timezone.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank = True, null = True, on_delete = models.CASCADE, related_name='polls')
    is_part_of_event = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if self.event:
            self.is_part_of_event = True
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 300)
    votes = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('date created', default = timezone.now)
    explanation = models.TextField(null = True, blank = True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_date = models.DateTimeField('date voted', default = timezone.now)
    choice_no = models.IntegerField(null = True, blank = True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class Comment(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    comment_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date commented')
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Comment of Question{}').format(self.question.id)
