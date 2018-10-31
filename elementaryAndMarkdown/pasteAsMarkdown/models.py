from django.db import models

# Create your models here.


class Pastebin(models.Model):
    markdown_text = models.TextField()
    path = models.CharField(max_length=34)
