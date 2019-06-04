from django.contrib.auth.models import AbstractUser
from django.db import models
from account.models import Account


class MyUser(AbstractUser):

    def __str__(self):
        return self.username

class UserInfo(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='info')
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
