from .models import Recipe
from django.contrib.auth.models import User
import random
from math import floor

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

    def get_random_meal(self, meal_type, calories_remaining=None):
        type_filter = {f"is_{meal_type}": True}
        meal_options = self.user_recipes.filter(**type_filter)
        if calories_remaining:
            meal_options = meal_options.filter(calories__lte=calories_remaining)
            if not meal_options:
                return None
        meal = random.choices(
            meal_options, weights=[meal.protein for meal in meal_options], k=1
        )
        return meal[0]

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
                breakfast, breakfast_servings = self.queue["breakfast"].pop(0)
            else:
                breakfast = self.get_random_meal("breakfast")
                breakfast_servings = breakfast.servings
            
            # set breakfast for the current day
            meal_plan.set_meal(breakfast, "breakfast")

            # if breakfast recipe has more than 1 serving, queue the meal for the next day
            if floor(breakfast_servings) > 1:
                self.queue["breakfast"].append((breakfast, breakfast_servings-1))

            # randomly pick a lunch
            if self.queue.get("lunch"):
                lunch, lunch_servings = self.queue["lunch"].pop(0)
            else:
                lunch = self.get_random_meal("lunch")
                lunch_servings = lunch.servings

            # set lunch for the current day
            meal_plan.set_meal(lunch, "lunch")

            # if lunch recipe has more than 1 serving, queue the meal for the next day
            if floor(lunch_servings) > 1:
                self.queue["lunch"].append((lunch, lunch_servings-1))   

            # randomly pick a dinner
            if self.queue.get("dinner"):
                dinner, dinner_servings = self.queue["dinner"].pop(0)
            else:
                dinner = self.get_random_meal("dinner")
                dinner_servings = dinner.servings

            # set dinner for the current day
            meal_plan.set_meal(dinner, "dinner")

            # if dinner recipe has more than 1 serving, queue the meal for the next day
            if floor(dinner_servings) > 1:
                self.queue["dinner"].append((dinner, dinner_servings-1))

            # calculate total calories for day

            # if total calories is less than daily limit, add snack
            if meal_plan.total_calories < self.daily_calorie_limit:
                snack = self.get_random_meal("snack", calories_remaining=self.daily_calorie_limit-meal_plan.total_calories)
                if snack:
                    meal_plan.set_meal(snack, "snack")

            # append MealPlan to list of meal plans
            meal_plans.append(meal_plan)

        return meal_plans
    

class IngredientList:

    def __init__(self, meal_plans):
        self.meal_plans = meal_plans
        self.ingredient_list = {}

    def execute(self):
        """
        Algorithm:
            For each meal plan, get the ingredients
            For each ingredient, add the quantity to the total
        """
        for meal_plan in self.meal_plans:
            for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                recipe = getattr(meal_plan, meal_type)
                if recipe:
                    for r_ingredient in recipe.recipeingredient_set.all():
                        if r_ingredient.ingredient.name not in self.ingredient_list:
                            self.ingredient_list[r_ingredient.ingredient.name] = {
                                "quantity": r_ingredient.quantity or 0,
                                "unit": r_ingredient.unit,
                            }
                        else:
                            self.ingredient_list[r_ingredient.ingredient.name]["quantity"] += (r_ingredient.quantity or 0)
        return self.ingredient_list


    
