from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ('user', 'date_created')

class MealPlannerForm(forms.Form):
    days_to_plan = forms.IntegerField()
    daily_calorie_limit = forms.IntegerField()