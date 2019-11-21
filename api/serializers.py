from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Review, Dish, Menu, Cafeteria, Organization

# User Drawer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'organization', 'review_cnt',)

# Review List Page & Review create Page

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('organization',)

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ReviewSerializer(serializers.ModelSerializer):
    written_by = SimpleUserSerializer()
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
