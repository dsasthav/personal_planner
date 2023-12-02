from .models import Meal 
from django.contrib.auth.models import User
import random

class MealPlanner:

    def __init__(self, user: User, days_to_plan: int, daily_calorie_limit: int):
        self.user = user
        self.days_to_plan = days_to_plan
        self.daily_calorie_limit = daily_calorie_limit
        self.user_meals = Meal.objects.filter(user=user)
    
    # Plan one day of meals based on calorie limit
    # randomly fetch breakfast, lunch, dinner, and add snack if below calorie limit
    def plan_one_day(self):
        
        # fetch breakfast options
        breakfast_options = self.user_meals.filter(is_breakfast=True)
    
        # fetch lunch options
        lunch_options = self.user_meals.filter(is_lunch=True)

        # fetch dinner options
        dinner_options = self.user_meals.filter(is_dinner=True)

        # randomly choose one list item from each meal type
        breakfast = random.choices(breakfast_options, weights = [meal.protein for meal in breakfast_options], k=1)[0]
        lunch = random.choice(lunch_options)
        dinner = random.choice(dinner_options)

        # calculate total calories + protein
        total_calories = breakfast.calories + lunch.calories + dinner.calories
        total_protein = breakfast.protein + lunch.protein + dinner.protein

        # if total calories is less than daily limit, add snack
        if total_calories < self.daily_calorie_limit:
            snack_options = self.user_meals.filter(is_snack=True)
            snack = random.choice(snack_options)
            total_calories += snack.calories
            total_protein += snack.protein
        else:
            snack = None
        
        return {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'snack': snack,
            'total_calories': total_calories,
            'total_protein': total_protein,
        }

    # Plan multiple days of meals based on calorie limit
    def execute(self):
        days = []
        for i in range(self.days_to_plan):
            days.append(self.plan_one_day())
        return days


        
        



        
        