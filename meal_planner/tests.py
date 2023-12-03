from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Recipe, Ingredient, RecipeIngredient

from django.urls import reverse
from .views import run_meal_planner, user_can_meal_plan, IngredientListView, IngredientDetailView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView, RecipeListView, UserRecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView


class RecipeModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            name='Test Recipe',
            calories=500,
            protein=30,
            servings=2.5,
            directions='Test directions',
            date_created=timezone.now(),
            is_breakfast=True,
            user=self.user,
            prep_time=15,
            cook_time=30,
            ready_time=45,
            ingredient_text='Test ingredient text',
        )

        self.assertEqual(recipe.name, 'Test Recipe')
        self.assertEqual(recipe.calories, 500)
        self.assertEqual(recipe.protein, 30)
        self.assertEqual(recipe.servings, 2.5)
        self.assertEqual(recipe.directions, 'Test directions')
        self.assertEqual(recipe.date_created.date(), timezone.now().date())
        self.assertTrue(recipe.is_breakfast)
        self.assertFalse(recipe.is_lunch)
        self.assertFalse(recipe.is_dinner)
        self.assertFalse(recipe.is_snack)
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.prep_time, 15)
        self.assertEqual(recipe.cook_time, 30)
        self.assertEqual(recipe.ready_time, 45)
        self.assertEqual(recipe.ingredient_text, 'Test ingredient text')

    def test_recipe_str_method(self):
        recipe = Recipe.objects.create(name='Test Recipe', user=self.user)
        self.assertEqual(str(recipe), 'Test Recipe')

    def test_recipe_get_absolute_url(self):
        recipe = Recipe.objects.create(name='Test Recipe', user=self.user)
        url = recipe.get_absolute_url()
        self.assertEqual(url, f'/recipe/{recipe.pk}/')  # Adjust the URL based on your URL configuration

class IngredientModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            date_created=timezone.now(),
            user=self.user,
        )

        self.assertEqual(ingredient.name, 'Test Ingredient')
        self.assertEqual(ingredient.date_created.date(), timezone.now().date())
        self.assertEqual(ingredient.user, self.user)

    def test_ingredient_str_method(self):
        ingredient = Ingredient.objects.create(name='Test Ingredient', user=self.user)
        self.assertEqual(str(ingredient), 'Test Ingredient')

    def test_ingredient_get_absolute_url(self):
        ingredient = Ingredient.objects.create(name='Test Ingredient', user=self.user)
        url = ingredient.get_absolute_url()
        self.assertEqual(url, f'/ingredient/{ingredient.pk}/')  # Adjust the URL based on your URL configuration

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a recipe and ingredient for testing
        self.recipe = Recipe.objects.create(name='Test Recipe', user=self.user)
        self.ingredient = Ingredient.objects.create(name='Test Ingredient', user=self.user)

    def test_recipeingredient_creation(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=2.5,
            unit='cups',
            date_created=timezone.now(),
        )

        self.assertEqual(recipe_ingredient.recipe, self.recipe)
        self.assertEqual(recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(recipe_ingredient.quantity, 2.5)
        self.assertEqual(recipe_ingredient.unit, 'cups')
        self.assertEqual(recipe_ingredient.date_created.date(), timezone.now().date())

    def test_recipeingredient_str_method(self):
        recipe_ingredient = RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient)
        self.assertEqual(str(recipe_ingredient), 'Test Recipe - Test Ingredient')


class MealPlannerViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_run_meal_planner_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('meal-planner'), {'days_to_plan': 7, 'daily_calorie_limit': 2000})
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_user_can_meal_plan_function(self):
        # Create a recipe for each meal type for the user
        Recipe.objects.create(name='Test Breakfast', is_breakfast=True, user=self.user)
        Recipe.objects.create(name='Test Lunch', is_lunch=True, user=self.user)
        Recipe.objects.create(name='Test Dinner', is_dinner=True, user=self.user)

        self.assertTrue(user_can_meal_plan(self.user))

    def test_user_cannot_meal_plan_function(self):
        # Create a recipe for only one meal type for the user
        Recipe.objects.create(name='Test Breakfast', is_breakfast=True, user=self.user)

        self.assertFalse(user_can_meal_plan(self.user))

class IngredientViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ingredient = Ingredient.objects.create(name='Test Ingredient', user=self.user)

    def test_ingredient_list_view(self):
        response = self.client.get(reverse('ingredient-list'))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_ingredient_detail_view(self):
        response = self.client.get(reverse('ingredient-detail', args=[str(self.ingredient.id)]))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_ingredient_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('ingredient-create'), {'name': 'New Ingredient'})
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_ingredient_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('ingredient-update', args=[str(self.ingredient.id)]), {'name': 'Updated Ingredient'})
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_ingredient_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('ingredient-delete', args=[str(self.ingredient.id)]))
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed

class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(name='Test Recipe', user=self.user)

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_user_recipe_list_view(self):
        response = self.client.get(reverse('user-recipe-list', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_recipe_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-create'), {'name': 'New Recipe'})
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-update', args=[str(self.recipe.id)]), {'name': 'Updated Recipe'})
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-delete', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed
