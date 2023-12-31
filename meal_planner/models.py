from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.IntegerField()
    protein = models.IntegerField()
    servings = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
    directions = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_breakfast = models.BooleanField(default=False)
    is_lunch = models.BooleanField(default=False)
    is_dinner = models.BooleanField(default=False)
    is_snack = models.BooleanField(default=False)
    prep_time = models.IntegerField(blank=True, null=True)
    cook_time = models.IntegerField(blank=True, null=True)
    ready_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField("Ingredient", through="RecipeIngredient")
    ingredient_text = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ingredient-detail", kwargs={"pk": self.pk})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
    unit = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"

    def get_absolute_url(self):
        return reverse("recipeingredient-detail", kwargs={"pk": self.pk})
