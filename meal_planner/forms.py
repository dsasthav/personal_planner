from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe, Ingredient, RecipeIngredient
from betterforms.multiform import MultiModelForm
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper

DEFAULT_DAYS_TO_PLAN = 5
DEFAULT_DAILY_CALORIE_LIMIT = 2000

class MealPlannerForm(forms.Form):
    days_to_plan = forms.IntegerField(initial=DEFAULT_DAYS_TO_PLAN, max_value=7, min_value=1)
    daily_calorie_limit = forms.IntegerField(initial=DEFAULT_DAILY_CALORIE_LIMIT, min_value=1000, max_value=5000)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
        exclude = ("date_created", "ingredients")

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Div(
                Field("subject"),
                Field("owner"),
                Fieldset(
                    "Add titles",
                    Field("note"),
                    HTML("<br>"),
                    ButtonHolder(Submit("submit", "Save")),
                ),
            )
        )


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity", "unit"]


RecipeIngredientFormset = forms.inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    max_num=20,
    can_delete=True,
)
