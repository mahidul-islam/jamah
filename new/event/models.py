from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import Blog
from jamah.models import Jamah
import uuid
import math


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
    is_responsible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.status=='member':
            self.is_responsible = True
        super(EventMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.member.username

class Cost(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default = timezone.now, editable=False)
    has_extracted_money = models.BooleanField(default = False)
    objected_by = models.ManyToManyField(EventMember, related_name='approved_costs', blank=True)
    cost_bearer = models.ManyToManyField(EventMember, blank=True)
    per_head_cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    is_objected = models.BooleanField(default = False)
    added_by = models.ForeignKey(EventMember, on_delete=models.CASCADE, related_name='created_costs')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.id:
            if self.objected_by.count():
                self.is_objected = True
        super(Cost, self).save(*args, **kwargs)

class TransactionIn(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    comes_from = models.ForeignKey(EventMember, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    is_donation = models.BooleanField(default=False)
    part_of_cost = models.ForeignKey(Cost, on_delete=models.CASCADE, related_name='cost_transaction_ins')

class TransactionOut(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    goes_to = models.ForeignKey(EventMember, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
