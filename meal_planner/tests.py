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
        self.recipe = Recipe.objects.create(
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

    def test_recipe_creation(self):
        

        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.calories, 500)
        self.assertEqual(self.recipe.protein, 30)
        self.assertEqual(self.recipe.servings, 2.5)
        self.assertEqual(self.recipe.directions, 'Test directions')
        self.assertEqual(self.recipe.date_created.date(), timezone.now().date())
        self.assertTrue(self.recipe.is_breakfast)
        self.assertFalse(self.recipe.is_lunch)
        self.assertFalse(self.recipe.is_dinner)
        self.assertFalse(self.recipe.is_snack)
        self.assertEqual(self.recipe.user, self.user)
        self.assertEqual(self.recipe.prep_time, 15)
        self.assertEqual(self.recipe.cook_time, 30)
        self.assertEqual(self.recipe.ready_time, 45)
        self.assertEqual(self.recipe.ingredient_text, 'Test ingredient text')

    def test_recipe_str_method(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_recipe_get_absolute_url(self):
        url = self.recipe.get_absolute_url()
        self.assertEqual(url, f'/meal_planner/recipe/{self.recipe.pk}/')  # Adjust the URL based on your URL configuration

class IngredientModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            date_created=timezone.now(),
            user=self.user,
        )

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, 'Test Ingredient')
        self.assertEqual(self.ingredient.date_created.date(), timezone.now().date())
        self.assertEqual(self.ingredient.user, self.user)

    def test_ingredient_str_method(self):
        self.assertEqual(str(self.ingredient), 'Test Ingredient')

    def test_ingredient_get_absolute_url(self):
        url = self.ingredient.get_absolute_url()
        self.assertEqual(url, f'/meal_planner/ingredient/{self.ingredient.pk}/')  # Adjust the URL based on your URL configuration

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a recipe and ingredient for testing
        self.recipe = Recipe.objects.create(
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
        self.ingredient = Ingredient.objects.create(name='Test Ingredient', user=self.user)

        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=2.5,
            unit='cups',
            date_created=timezone.now(),
        )

    def test_recipeingredient_creation(self):
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(self.recipe_ingredient.quantity, 2.5)
        self.assertEqual(self.recipe_ingredient.unit, 'cups')
        self.assertEqual(self.recipe_ingredient.date_created.date(), timezone.now().date())

    def test_recipeingredient_str_method(self):
        self.assertEqual(str(self.recipe_ingredient), 'Test Recipe - Test Ingredient')


class MealPlannerViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_run_meal_planner_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('meal-planner'), {'days_to_plan': 7, 'daily_calorie_limit': 2000})
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

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
        self.recipe = Recipe.objects.create(
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

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_user_recipe_list_view(self):
        response = self.client.get(reverse('user-recipes', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

    def test_recipe_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-create'), {'name': 'New Recipe'})
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-update', args=[str(self.recipe.id)]), {'name': 'Updated Recipe'})
        self.assertEqual(response.status_code, 200)  # Adjust based on your expected status code

        # Test other scenarios as needed

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-delete', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 302)  # Adjust based on your expected status code

        # Test other scenarios as needed
