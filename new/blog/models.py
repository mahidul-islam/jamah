from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Blog(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    heading_text = models.CharField(max_length = 200)
    body_text = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(default = timezone.now)
    is_finished = models.BooleanField(default = False)
    is_published = models.BooleanField(default = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return self.heading_text

class VoteForBlog(models.Model):
    uid = models.UUIDField(  default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
