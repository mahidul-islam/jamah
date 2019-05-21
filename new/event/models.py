from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import Blog
from jamah.models import Jamah
import uuid


class Account(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

class Event(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'created_events')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)
    is_donation_only_event = models.BooleanField(default = False)
    # official_blog = models.OneToOneField(Blog, on_delete=models.CASCADE, blank=True, null=True)
    jamah = models.ForeignKey(Jamah, on_delete=models.CASCADE, related_name = 'events')

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

class Cost(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default = timezone.now)
    added_by = models.ForeignKey(EventMember, on_delete=models.CASCADE, related_name='creator')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    per_head_cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    extracted_money = models.BooleanField(default = False)
    cost_bearer = models.ManyToManyField(EventMember, blank=True)

class TransactionIn(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    comes_from = models.ForeignKey(EventMember, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    is_donation = models.BooleanField(default=False)
    part_of_cost = models.ForeignKey(Cost, on_delete=models.CASCADE, default=None)

class TransactionOut(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    goes_to = models.ForeignKey(EventMember, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
