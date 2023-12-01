from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import MealForm
from .models import Meal
PAGINATE_NUM = 10


class MealListView(ListView):
    model = Meal
    ordering = ['-date_created']
    paginate_by = PAGINATE_NUM


class UserMealListView(ListView):
    model = Meal
    template_name = 'meal/user_meals.html'  # <app>/<model>_<viewtype>.html
    paginate_by = PAGINATE_NUM

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Meal.objects.filter(user=user).order_by('-date_created')


class MealDetailView(DetailView):
    model = Meal


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    form_class = MealForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meal
    form_class = MealForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    success_url = '/meal'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False