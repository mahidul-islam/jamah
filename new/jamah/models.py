import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Jamah(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable=False)
    jamahname = models.CharField(max_length = 255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jamahs_of_you')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    timestamp = models.DateTimeField(default = timezone.now, editable=False)
    requested_to_join = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='requested_jamah')

    def __str__(self):
        return self.jamahname

STATUS_CHOICES = (
    ('creator', 'CREATOR'),
    ('modarator','MODARATOR'),
    ('admin','ADMIN'),
    ('member','MEMBER'),
)

class JamahMember(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='member')
    jamah = models.ForeignKey(Jamah, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = timezone.now, editable=False)
    still_to_be_excepted = models.BooleanField(default = True)
    is_responsible = models.BooleanField(default=False)

    def __str__(self):
        return self.member.username

def save(self, *args, **kwargs):
    if not self.status=='member':
        self.is_responsible = True
    super(JamahMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.member.username
