from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, Recipe, Ingredient
from .serializers import IngredientSerializer, RecipeSerializer, \
    RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False, url_path='by-recipe/(?P<recipe_id>\d+)')
    def by_recipe(self, request, recipe_id=None):
        restaurants = Restaurant.objects.filter(recipes__id=recipe_id)
        serializer = self.get_serializer(restaurants, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('restaurant').prefetch_related(
        'ingredients')
    serializer_class = RecipeSerializer

    @action(detail=False, url_path='by-restaurant/(?P<restaurant_id>\d+)')
    def by_restaurant(self, request, restaurant_id=None):
        recipes = Recipe.objects.filter(
            restaurant__id=restaurant_id).select_related('restaurant')
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='by-ingredient/(?P<ingredient_id>\d+)')
    def by_ingredient(self, request, ingredient_id=None):
        recipes = Recipe.objects.filter(ingredients__id=ingredient_id).select_related('restaurant').prefetch_related('ingredients')
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    @action(detail=False, url_path='by-recipe/(?P<recipe_id>\d+)')
    def by_recipe(self, request, recipe_id=None):
        ingredients = Ingredient.objects.filter(recipes__id=recipe_id).prefetch_related('recipes__restaurant')
        serializer = self.get_serializer(ingredients, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='by-restaurant/(?P<restaurant_id>\d+)')
    def by_restaurant(self, request, restaurant_id=None):
        ingredients = Ingredient.objects.filter(recipes__restaurant__id=restaurant_id).prefetch_related('recipes__restaurant')
        serializer = self.get_serializer(ingredients, many=True)
        return Response(serializer.data)


'''
1. 
recipe = Recipe.objects.filter(name="XXX").first()
recipe.name = "YYY"
recipe.save()

UPDATE recipe SET recipe.name = "YYY" recipe.ingredients = ...; 

2. 

recipe = Recipe.objects.filter(name="XXX").first()
recipe.name = "YYY"
recipe.save(update_fields=["name"])

3.

Recipe.objects.filter(name="XX").update(name="YYY")
'''