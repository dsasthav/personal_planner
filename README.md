# Django Meal Planner README

Welcome to my personal Meal Planner app! This application allows users to enter recipes and ingredients and generates a weekly meal plan along with a shopping list.

## Table of Contents

1. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
2. [Running the App](#running-the-app)
3. [Data Model](#data-model)
   - [Recipe Model](#recipe-model)
   - [Ingredient Model](#ingredient-model)
   - [RecipeIngredient Model](#recipeingredient-model)
4. [Usage](#usage)
   - [Entering Recipes and Ingredients](#entering-recipes-and-ingredients)
   - [Generating Meal Plan](#generating-meal-plan)
   - [Viewing Shopping List](#viewing-shopping-list)

## Setup

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.11.6
- pip (Python package installer)
- virtualenv (optional but recommended for creating a virtual environment)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dsasthav/personal_planner.git
   cd personal_planner
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

## Running the App

To run the Django Meal Planner app locally, use the following command:

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your web browser to access the application.

## Data Model

### Recipe Model (key fields)

- `name` (CharField): The name of the recipe.
- `calories` (IntegerField): Amount of calories in the recipe
- `protein` (IntegerField): Grams of protein in recipe
- `directions` (TextField): Detailed cooking instructions for the recipe.

### Ingredient Model

- `name` (CharField): The name of the ingredient.

### RecipeIngredient Model

- `recipe` (ForeignKey to Recipe): The recipe associated with the ingredient.
- `ingredient` (ForeignKey to Ingredient): The ingredient used in the recipe.
- `quantity` (FloatField): The quantity of the ingredient needed in the recipe.
- `unit` (CharField): unit of measurement

## Usage

### Entering Recipes and Ingredients

1. Navigate to the Django admin interface [http://localhost:8000/admin](http://localhost:8000/admin).
2. Log in with your superuser credentials.
3. Add recipes and ingredients through the admin interface.

### Generating Meal Plan

1. Visit [http://localhost:8000/meal_planner](http://localhost:8000/meal-plan).
2. Enter in the number of days to plan and the daily calorie limit
2. Click the "Submit" button to create a weekly meal plan.

### Viewing Shopping List

1. After generating the meal plan, scroll down to view the Ingredient List

Enjoy using the Django Meal Planner app! If you encounter any issues or have suggestions, please feel free to raise them on the [GitHub repository](https://github.com/dsasthav/personal_planner.git).