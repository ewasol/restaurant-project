from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...models import Restaurant, Ingredient, Recipe
from ...serializers import IngredientSerializer


class IngredientViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.restaurant1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant2 = Restaurant.objects.create(name="Restaurant 2")

        self.ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="Ingredient 2")

        self.recipe1 = Recipe.objects.create(name="Recipe 1", restaurant=self.restaurant1)
        self.recipe1.ingredients.add(self.ingredient1)

        self.recipe2 = Recipe.objects.create(name="Recipe 2", restaurant=self.restaurant2)
        self.recipe2.ingredients.add(self.ingredient2)

    def test_should_get_ingredients_by_recipe_with_matching_recipe_id(self):
        url = reverse('ingredient-by-recipe', args=[self.recipe1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(recipes__id=self.recipe1.id).prefetch_related('recipes').distinct()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_empty_list_when_no_matching_recipe_id(self):
        url = reverse('ingredient-by-recipe', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(
            restaurant__id=999).prefetch_related('recipes').distinct()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_ingredients_by_restaurant_with_matching_restaurant_id(self):
        url = reverse('ingredient-by-restaurant', args=[self.restaurant1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(
            recipes__id=self.restaurant1.id).prefetch_related(
            'recipes').distinct()
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_should_get_empty_list_when_no_matching_restaurant_id(self):
        url = reverse('ingredient-by-restaurant', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(recipes__restaurant__id=999).prefetch_related('recipes__restaurant').distinct()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.data, serializer.data)

