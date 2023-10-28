import os

from django.contrib.auth.models import User
from django.db import models

from fan_server import settings


class AnnouncementCategory(models.Model):
    """
    Категория объявлений
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pk} {self.title}"


class Announcement(models.Model):
    """
    Объявления
    """
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnnouncementMedia(models.Model):
    """
    Объявления
    """
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    media = models.FileField(upload_to=settings.MEDIA_ROOT)


class Comment(models.Model):
    """
    Ответы на Объявления
    """
    text = models.TextField()
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
