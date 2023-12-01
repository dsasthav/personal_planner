from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Meal(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField(blank=True)
    recipe = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_breakfast = models.BooleanField(default=False)
    is_lunch = models.BooleanField(default=False)
    is_dinner = models.BooleanField(default=False)
    is_snack = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('meal-detail', kwargs={'pk': self.pk})
