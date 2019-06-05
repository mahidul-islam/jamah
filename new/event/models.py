from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import Blog
from jamah.models import Jamah
from account.models import Account
import uuid
import math


class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'created_events')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    account = models.OneToOneField(Account, on_delete = models.CASCADE, related_name='event_for_account')
    cost_account = models.OneToOneField(Account, on_delete = models.CASCADE, related_name='event_for_cost_account')
    is_donation_only_event = models.BooleanField(default = False)
    jamah = models.ForeignKey(Jamah, on_delete=models.CASCADE, related_name = 'events')
    resposible_member_count = models.IntegerField(default=1)
    modarator_member_count = models.IntegerField(default=0)
    admin_member_count = models.IntegerField(default=0)
    per_head_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_donation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_recieved_money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    event_finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.id:
            self.per_head_cost = math.ceil(self.total_cost/self.members.count())
        super(Event, self).save(*args, **kwargs)

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
    accountant_account = models.OneToOneField(Account, on_delete = models.CASCADE, blank=True, null=True)
    is_accountant = models.BooleanField(default=False)
    is_cost_observer = models.BooleanField(default=False)
    total_verified = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_sent_money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_donation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.event.members.add(self.member)
        if not self.status=='member':
            self.is_responsible = True
        super(EventMember, self).save(*args, **kwargs)

    def __str__(self):
        return ('{} --- \"{}\"').format(self.member.username, self.event.name)

class Cost(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default = timezone.now, editable=False)
    objected_by = models.ManyToManyField(EventMember, related_name='objected_costs', blank=True)
    is_objected = models.BooleanField(default = False)
    added_by = models.ForeignKey(EventMember, on_delete=models.CASCADE, related_name='created_costs')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_observed = models.BooleanField(default=False)
    observed_by = models.ForeignKey(EventMember, related_name='observed_costs', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Cost, self).save(*args, **kwargs)
