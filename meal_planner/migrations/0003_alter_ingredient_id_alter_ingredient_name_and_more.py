# Generated by Django 4.2.7 on 2023-12-03 03:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meal_planner", "0002_ingredient_recipe_recipeingredient_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.DeleteModel(
            name="Meal",
        ),
    ]
