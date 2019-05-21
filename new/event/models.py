from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import Blog
import uuid


class Account(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

class TransactionIn(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    comes_from = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

class TransactionOut(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    goes_to = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

class Event(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'Boss')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)
    is_donation_only_event = models.BooleanField(default = False)
    official_blog = models.OneToOneField(Blog, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

STATUS_CHOICES = (
    ('creator', 'CREATOR'),
    ('modarator','MODARATOR'),
    ('admin','ADMIN'),
    ('member','MEMBER'),
)

class EventMember(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='member')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = timezone.now, editable=False)

    def __str__(self):
        return self.member.username
