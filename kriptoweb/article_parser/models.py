from django.db import models


# Create your models here.
class Sources(models.Model):
    type = models.CharField(max_length=255)
    url = models.TextField()


class Patterns(models.Model):
    datetime = models.DateTimeField()
    imgSource = models.ManyToManyField(Sources)
    title = models.TextField(default="noTitle")
    content = models.TextField()

    class Meta:
        ordering = ['datetime']
