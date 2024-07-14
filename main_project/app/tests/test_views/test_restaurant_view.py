from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ...models import Recipe, Restaurant
from ...serializers import RestaurantSerializer


class RestaurantViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.recipe1 = Recipe.objects.create(name="Recipe 1")
        self.recipe2 = Recipe.objects.create(name="Recipe 2")

        self.restaurant1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant2 = Restaurant.objects.create(name="Restaurant 2")

        self.restaurant1.recipes.add(self.recipe1)
        self.restaurant2.recipes.add(self.recipe2)

    def test_should_get_restaurants_by_recipe_with_matching_recipe_id(self):
        url = reverse('restaurant-by-recipe', args=[self.recipe1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        restaurants = Restaurant.objects.filter(recipes__id=self.recipe1.id)
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_get_empty_list_when_no_matching_recipe_id(self):
        url = reverse('restaurant-by-recipe', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        restaurants = Restaurant.objects.filter(recipes__id=999)
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_should_raise_404_when_invalid_recipe_id(self):
        url = reverse('restaurant-by-recipe', args=["invalid"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
