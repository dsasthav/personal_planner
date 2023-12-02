from .models import Meal 
from django.contrib.auth.models import User
import random

class DayMeals:
    def __init__(self):
        self.breakfast = None
        self.breakfast_servings = 0
        self.lunch = None
        self.lunch_servings = 0
        self.dinner = None
        self.dinner_servings = 0
        self.snack = None
        self.snack_servings = 0
        self.total_calories = 0
        self.total_protein = 0
    
    # setter for breakfast
    def set_breakfast(self, meal, qty=1):
        self.breakfast = meal
        self.breakfast_servings = qty
        self.total_calories += meal.calories*qty
        self.total_protein += meal.protein*qty

    # setter for lunch
    def set_lunch(self, meal, qty=1):
        self.lunch = meal
        self.lunch_servings = qty
        self.total_calories += meal.calories*qty
        self.total_protein += meal.protein*qty
    
    # setter for dinner
    def set_dinner(self, meal, qty=1):
        self.dinner = meal
        self.dinner_servings = qty
        self.total_calories += meal.calories*qty
        self.total_protein += meal.protein*qty

    # setter for snack
    def set_snack(self, meal, qty=1):
        self.snack = meal
        self.snack_servings = qty
        self.total_calories += meal.calories*qty
        self.total_protein += meal.protein*qty

    # method to check if breakfast, lunch, and dinner are set
    def is_complete(self):
        return self.breakfast and self.lunch and self.dinner
    

class MealPlanner:

    def __init__(self, user: User, days_to_plan: int, daily_calorie_limit: int, meal_calorie_minimum: int = 400):
        self.user = user
        self.days_to_plan = days_to_plan
        self.daily_calorie_limit = daily_calorie_limit
        self.user_meals = Meal.objects.filter(user=user)
        self.meal_calorie_minimum = meal_calorie_minimum
        self.week_meals = [DayMeals() for _ in range(days_to_plan) ]

    # Plan multiple days of meals based on calorie limit
    def execute(self):
        # for each day to plan
        for day_num, day in enumerate(self.week_meals):
            # pick a breakfast
            if not day.breakfast:
                breakfast_options = self.user_meals.filter(is_breakfast=True)
                breakfast = random.choices(breakfast_options, weights = [meal.protein for meal in breakfast_options], k=1)[0]
                breakfast_servings_to_eat = self.choose_daily_servings(breakfast)
                day.set_breakfast(breakfast, breakfast_servings_to_eat)

                 

            # pick a lunch
            if not day.lunch:
                lunch_options = self.user_meals.filter(is_lunch=True)
                lunch = random.choices(lunch_options, weights = [meal.protein for meal in lunch_options], k=1)[0]
                lunch_servings_to_eat = self.choose_daily_servings(lunch)
                day.set_lunch(lunch, lunch_servings_to_eat)

                # if lunch recipe makes more than 1 day of servings, add to next day
                if lunch_servings_to_eat < lunch.servings and self.week_meals.index(day) < len(self.week_meals) - 1:
                    self.week_meals[self.week_meals.index(day) + 1].set_lunch(lunch, lunch_servings_to_eat)

            # pick a dinner
            if not day.dinner:
                dinner_options = self.user_meals.filter(is_dinner=True)
                dinner = random.choices(dinner_options, weights = [meal.protein for meal in dinner_options], k=1)[0]
                dinner_servings = self.choose_daily_servings(dinner)
                day.set_dinner(dinner, dinner_servings)

                # if dinner recipe makes more than 1 day of servings, add to next day
                if dinner_servings > 1 and self.week_meals.index(day) < len(self.week_meals) - 1:
                    self.week_meals[self.week_meals.index(day) + 1].set_dinner(dinner, dinner_servings)
            
            # calculate total calories
            if day.total_calories < self.daily_calorie_limit:
                snack_options = self.user_meals.filter(is_snack=True)
                snack = random.choice(snack_options)
                day.set_snack(snack, 1)
            
        return self.week_meals
        

    # choose the daily servings of the meal type to get at least 500 calories
    def choose_daily_servings(self, meal):
        calories_per_serving = meal.calories
        meal_calories = meal.calories
        servings_per_day = 1
        while meal_calories < self.meal_calorie_minimum:
            servings_per_day += 1
            meal_calories = servings_per_day * calories_per_serving
        return servings_per_day


        
        



        
        