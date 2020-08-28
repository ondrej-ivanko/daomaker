from django.db import models


class Task(models.Model):
    parsed_url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    site_name = models.CharField(max_length=255, blank=True)
    image_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
