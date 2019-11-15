from rest_framework import serializers

from .models import *


# Review List Page & Review create Page

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating


# class ReviewSerializer(serializers.ModelSerializer):
#     rating =
#     class Meta:
#         model = Review
#         fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    # review_set = ReviewSerializer(many=True)

    class Meta:
        model = Dish
        fields = '__all__'


# Cafeteria Page (Menu List)
class SimpleDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'avg_rating')


class MenuSerializer(serializers.ModelSerializer):
    dishes = SimpleDishSerializer(many=True)

    class Meta:
        model = Menu
        fields = '__all__'


class CafeteriaSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True)

    class Meta:
        model = Cafeteria
        fields = '__all__'


# Cafeteria List Page
class BelongsToSerializer(serializers.ModelSerializer):
    cafeterias = CafeteriaSerializer(many=True)

    class Meta:
        model = BelongsTo
        fields = '__all__'
