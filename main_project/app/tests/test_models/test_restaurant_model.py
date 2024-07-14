from django.test import TestCase
from ...models import Restaurant


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

    def test_should_return_string_representation(self):
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

    def test_should_create_restaurant(self):
        restaurant = Restaurant.objects.create(name='New Restaurant')
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(restaurant.name, 'New Restaurant')
