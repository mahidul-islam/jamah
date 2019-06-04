from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid

class Account(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    mother_account = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='member_accounts')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Transaction(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_donation = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    comes_from = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='transaction_outs', null=True, blank=True)
    goes_to = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='transaction_ins')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='verified_transaction')
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
