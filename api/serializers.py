from rest_framework import serializers

from .models import *


# Review List Page & Review create Page

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'level')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Dish
        fields = '__all__'


# Cafeteria Page (Menu List)
class SimpleDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'rating_sum', 'rating_count')


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
class OrganizationSerializer(serializers.ModelSerializer):
    cafeterias = CafeteriaSerializer(many=True)

    class Meta:
        model = Organization
        fields = '__all__'
