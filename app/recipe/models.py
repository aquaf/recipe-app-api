from django.db import models

from django.conf import settings


class Tag(models.Model):
    """Tag to be used for recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    """Ingridient that uses in recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
