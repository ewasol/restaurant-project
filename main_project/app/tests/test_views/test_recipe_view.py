from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...models import Restaurant, Ingredient, Recipe
from ...serializers import RecipeSerializer


class RecipeViewSetTests(TestCase):
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

    def test_should_get_recipes_by_restaurant_with_matching_restaurant_id(self):
        url = reverse('recipe-by-restaurant', args=[self.restaurant1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(restaurant__id=self.restaurant1.id).prefetch_related('ingredients')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_empty_list_when_no_matching_restaurant_id(self):
        url = reverse('recipe-by-restaurant', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(restaurant__id=999).prefetch_related('ingredients')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_recipes_by_ingredient_with_matching_ingredient_id(self):
        url = reverse('recipe-by-ingredient', args=[self.ingredient1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(ingredients__id=self.ingredient1.id).select_related('restaurant').prefetch_related('ingredients').distinct()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_empty_list_when_no_matching_ingredient_id(self):
        url = reverse('recipe-by-ingredient', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(ingredients__id=999).select_related('restaurant').prefetch_related('ingredients').distinct()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.data, serializer.data)
