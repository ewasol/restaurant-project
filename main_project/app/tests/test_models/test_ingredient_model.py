from django.test import TestCase
from ...models import Ingredient


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')

    def test_should_return_string_representation(self):
        self.assertEqual(str(self.ingredient), 'Test Ingredient')

    def test_should_create_ingredient(self):
        ingredient = Ingredient.objects.create(name='New Ingredient')
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertEqual(ingredient.name, 'New Ingredient')
