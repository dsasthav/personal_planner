from django.urls import path
from .views import (
    MealListView,
    MealDetailView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
    UserMealListView
)
from . import views

urlpatterns = [
    path('', MealListView.as_view(), name='meal-list'),
    path('user/<str:username>', UserMealListView.as_view(), name='user-meals'),
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('meal/new/', MealCreateView.as_view(), name='meal-create'),
    path('meal/<int:pk>/update/', MealUpdateView.as_view(), name='meal-update'),
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),
]