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


class Recipe(models.Model):
    """Recipe object"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.SmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingridiets = models.ManyToManyField("Ingridient", related_name="recipe")
    tags = models.ManyToManyField("Tag", related_name="recipe")

    def __str__(self):
        return self.title
