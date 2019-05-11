from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Account(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

class TransactionIn(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    comes_from = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)

class TransactionOut(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    goes_to = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)

class Event(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'Boss')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
