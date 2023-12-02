from django.urls import path
from .views import (
    MealListView,
    MealDetailView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
    UserMealListView,
    run_meal_planner,
    IngredientListView,
    IngredientDetailView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    UserRecipeListView,
)
from . import views

urlpatterns = [
    path('', run_meal_planner, name='meal-planner'),
    path('meal', MealListView.as_view(), name='meal-list'),
    path('user/<str:username>', UserMealListView.as_view(), name='user-meals'),
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('meal/new/', MealCreateView.as_view(), name='meal-create'),
    path('meal/<int:pk>/update/', MealUpdateView.as_view(), name='meal-update'),
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),

    path('ingredient', IngredientListView.as_view(), name='ingredient-list'),
    path('ingredient/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
    path('ingredient/new/', IngredientCreateView.as_view(), name='ingredient-create'),
    path('ingredient/<int:pk>/update/', IngredientUpdateView.as_view(), name='ingredient-update'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient-delete'),

    path('recipe', RecipeListView.as_view(), name='recipe-list'),
    path('user/<str:username>', UserRecipeListView.as_view(), name='user-recipes'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
]