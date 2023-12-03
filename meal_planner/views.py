from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import MealPlannerForm, RecipeForm, RecipeIngredientFormset
from .models import Ingredient, Recipe, RecipeIngredient
from .utils import MealPlanner, IngredientList
from django.db import transaction


PAGINATE_NUM = 10


@login_required
def run_meal_planner(request):
    context = {}
    if request.method == "POST":
        form = MealPlannerForm(request.POST)
        if form.is_valid():
            user = request.user
            days_to_plan = form.cleaned_data.get("days_to_plan")
            daily_calorie_limit = form.cleaned_data.get("daily_calorie_limit")
            meal_planner = MealPlanner(user, days_to_plan, daily_calorie_limit)
            if user_can_meal_plan(user):

                meal_plan = meal_planner.execute()
                ingredient_list = IngredientList(meal_plans=meal_plan).execute()
                context.update({"meal_plan": meal_plan,
                                "ingredient_list": dict(sorted(ingredient_list.items())),
                                })
                messages.success(
                    request,
                    f"{user.username}'s meal plan has been created for {days_to_plan} days of {daily_calorie_limit} calories!",
                )
            else:
                messages.warning(
                    request,
                    f"{user.username} needs at least 1 breakfast, lunch, and dinner recipe to run the meal planner.",
                )
    else:
        form = MealPlannerForm()

    context.update({"form": form})
    return render(request, "meal_planner/meal_planner.html", context)

def user_can_meal_plan(user):
    """
    user can only run the meal plan if they have at least one recipe
    for breakfast, lunch, and dinner
    """
    user_recipes = Recipe.objects.filter(user=user)
    return (
        user_recipes.filter(is_breakfast=True).exists()
        and user_recipes.filter(is_lunch=True).exists()
        and user_recipes.filter(is_dinner=True).exists()
    )

class IngredientListView(ListView):
    model = Ingredient
    ordering = ["-date_created"]
    paginate_by = PAGINATE_NUM


class IngredientDetailView(DetailView):
    model = Ingredient


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = ["name"]


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = ["name"]


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient

    def get_success_url(self) -> str:
        return reverse_lazy("ingredient-list")


class RecipeListView(ListView):
    model = Recipe
    ordering = ["-date_created"]
    paginate_by = PAGINATE_NUM


class UserRecipeListView(ListView):
    model = Recipe
    template_name = "meal/user_recipes.html"  # <app>/<model>_<viewtype>.html
    paginate_by = PAGINATE_NUM

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Recipe.objects.filter(user=user).order_by("-date_created")


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "meal_planner/recipe_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_formset"] = RecipeIngredientFormset(prefix="ingredient")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context["ingredient_formset"]

        with transaction.atomic():
            self.object = form.save()

            if ingredient_formset.is_valid():
                for form in ingredient_formset:
                    ingredient = form.save(commit=False)
                    ingredient.recipe = self.object
                    ingredient.save()

        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "meal_planner/recipe_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["ingredient_formset"] = RecipeIngredientFormset(
                self.request.POST, instance=self.object, prefix="ingredient"
            )
        else:
            context["ingredient_formset"] = RecipeIngredientFormset(
                instance=self.object, prefix="ingredient"
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context["ingredient_formset"]

        with transaction.atomic():
            self.object = form.save()

            if ingredient_formset.is_valid():
                for iform in ingredient_formset:
                    if iform.has_changed():

                        ingredient = iform.save(commit=False)
                        ingredient.recipe = (
                            self.object
                        )  # Set the relationship to the updated recipe
                        ingredient.save()
                ingredient_formset.save()  # Save the formset

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipe-detail", kwargs={"pk": self.object.pk})


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe-list")

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.user:
            return True
        return False
