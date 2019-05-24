from django.db import models
from django.utils import timezone
import uuid

class Account(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

class Transaction(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    comes_from = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='transaction_outs')
    goes_to = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='transaction_ins')
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
