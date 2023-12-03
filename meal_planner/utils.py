from .models import Recipe
from django.contrib.auth.models import User
import random


class MealPlan:
    """
    Meal plan for one day
    """
    def __init__(self, breakfast=None, lunch=None, dinner=None, snack=None):
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.snack = snack
        self.total_calories = 0
        self.total_protein = 0

    def set_meal(self, recipe, meal_type):
        setattr(self, meal_type, recipe)
        self.total_calories += recipe.calories 
        self.total_protein += recipe.protein

class MealPlanner:

    def __init__(
        self,
        user: User,
        days_to_plan: int,
        daily_calorie_limit: int,
        meal_calorie_minimum: int = 400,
    ):
        self.user = user
        self.days_to_plan = days_to_plan
        self.daily_calorie_limit = daily_calorie_limit
        self.user_recipes = Recipe.objects.filter(user=user)
        self.queue = {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
        }

    def get_random_meal(self, meal_type):
        filter = {f"is_{meal_type}": True}
        meal_options = self.user_recipes.filter(**filter)
        meal = random.choices(
            meal_options, weights=[meal.protein for meal in meal_options], k=1
        )[0]
        return meal

    def execute(self):
        """
        Algorithm:
            Every day needs a breakfast, lunch, and dinner
            For each meal, pick a random recipe from the user's recipes
            If the recipe has more than 1 serving, queue the recipe for the next day
            If the total calories for the day is less than the daily calorie limit, add a snack
        """
        
        meal_plans = []
        for _ in range(self.days_to_plan):
            meal_plan = MealPlan()
            
            # randomly pick a breakfast
            if self.queue.get("breakfast"):
                breakfast, breakfast_servings = self.queue.pop("breakfast")
            else:
                breakfast = self.get_random_meal("breakfast")
                breakfast_servings = breakfast.servings
            
            # set breakfast for the current day
            meal_plan.set_meal(breakfast, "breakfast")

            # if breakfast recipe has more than 1 serving, queue the meal for the next day
            if breakfast_servings > 1:
                self.queue["breakfast"].append((breakfast, breakfast_servings-1))

            # randomly pick a lunch
            if self.queue.get("lunch"):
                lunch, lunch_servings = self.queue.pop("lunch")
            else:
                lunch = self.get_random_meal("lunch")
                lunch_servings = lunch.servings

            # set lunch for the current day
            meal_plan.set_meal(lunch, "lunch")

            # if lunch recipe has more than 1 serving, queue the meal for the next day
            if lunch_servings > 1:
                self.queue["lunch"].append((lunch, lunch_servings-1))   

            # randomly pick a dinner
            if self.queue.get("dinner"):
                dinner, dinner_servings = self.queue.pop("dinner")
            else:
                dinner = self.get_random_meal("dinner")
                dinner_servings = dinner.servings

            # set dinner for the current day
            meal_plan.set_meal(dinner, "dinner")

            # if dinner recipe has more than 1 serving, queue the meal for the next day
            if dinner_servings > 1:
                self.queue["dinner"].append((dinner, dinner_servings-1))

            # calculate total calories for day

            # if total calories is less than daily limit, add snack
            if meal_plan.total_calories < self.daily_calorie_limit:
                snack = self.get_random_meal("snack")
                meal_plan.set_meal(snack, "snack")

            # append MealPlan to list of meal plans
            meal_plans.append(meal_plan)

        return meal_plans

    
