import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Jamah(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable=False)
    jamahname = models.CharField(max_length = 255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    timestamp = models.DateTimeField(default = timezone.now)
    requested_to_join = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.jamahname
