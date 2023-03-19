from django.conf import settings
from django.db import models
from django.utils import timezone


class Folder(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title