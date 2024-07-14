from django.test import TestCase
from ...models import Ingredient, Recipe, Restaurant


class RecipeModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.ingredient1 = Ingredient.objects.create(name='Ingredient 1')
        self.ingredient2 = Ingredient.objects.create(name='Ingredient 2')
        self.recipe = Recipe.objects.create(name='Test Recipe', restaurant=self.restaurant)
        self.recipe.ingredients.add(self.ingredient1, self.ingredient2)

    def test_should_return_string_representation(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_should_create_recipe(self):
        new_recipe = Recipe.objects.create(name='New Recipe', restaurant=self.restaurant)
        new_recipe.ingredients.add(self.ingredient1)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(new_recipe.name, 'New Recipe')
        self.assertEqual(new_recipe.restaurant, self.restaurant)
        self.assertEqual(new_recipe.ingredients.count(), 1)
        self.assertIn(self.ingredient1, new_recipe.ingredients.all())

    def test_should_retrieve_correct_number_of_ingredients_for_recipe(self):
        self.assertEqual(self.recipe.ingredients.count(), 2)

    def test_should_include_ingredient_in_recipe_ingredients(self):
        self.assertIn(self.ingredient1, self.recipe.ingredients.all())
        self.assertIn(self.ingredient2, self.recipe.ingredients.all())

    def test_should_associate_recipe_with_correct_restaurant(self):
        self.assertEqual(self.recipe.restaurant, self.restaurant)

    def test_should_include_recipe_in_restaurant_recipes(self):
        self.assertIn(self.recipe, self.restaurant.recipes.all())
