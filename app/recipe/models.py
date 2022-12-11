from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .helper import recipe_image_file_path


class Tag(models.Model):
    """ Tags used for a recipe """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredients used in a recipe """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField("Ingredient")  # rel to Ingredient models
    tags = models.ManyToManyField("Tag")  # rel to Tag models
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipe')
