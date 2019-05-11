from django.db import models
from django.conf import settings
from event.models import Event
import uuid
from django.db.models.signals import post_save


class Question(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, blank = True, null = True, on_delete = models.CASCADE)
    # TODO: made a signal for is part of event from event
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Choice for question {}').format(self.question.id)

class Voter(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice_no = models.IntegerField()

class Comment(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    comment_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date commented')
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return ('Comment of Question{}').format(self.question.id)


# def save_is_part_of_event_bool(sender, instance, **kwargs):
#     # print(sender)
#     if instance.event:
#         print('got it ...................... got it')
#         instance.is_part_of_event = True
#         print(instance.question_text)
#         print(instance.is_part_of_event)
#     instance.is
#
# post_save.connect(save_is_part_of_event_bool, sender=Question)
