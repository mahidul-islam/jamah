from django.db import models
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length = 100)
    creation_date = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length = 100)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    is_admin = models.BooleanField(default = False)

    def __str__(self):
        return self.name
