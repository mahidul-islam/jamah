from django.db import models
from django.conf import settings
from django.utils import timezone


class TransactionIn(models.Model):
    comes_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

class TransactionOut(models.Model):
    goes_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

class Account(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    transactionIns = models.ForeignKey(TransactionIn, on_delete = models.CASCADE)
    transactionOuts = models.ForeignKey(TransactionOut, on_delete = models.CASCADE)

class Event(models.Model):
    name = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'Boss')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    account = models.OneToOneField(Account, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
