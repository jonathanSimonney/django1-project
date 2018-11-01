from django.db import models
# Create your models here.


class Pastebin(models.Model):
    markdown_text = models.TextField()
    path = models.CharField(blank=True, unique=True, max_length=40)

    # safety check in the save method itself
    def save(self, *args, **kwargs):
        if self.path != '':
            super(Pastebin, self).save(*args, **kwargs)
        else:
            raise Exception("path should not be null")
