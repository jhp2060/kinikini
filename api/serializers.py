from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewUserSerializer(serializers.ModelSerializer):
    written_by = UserSerializer

    class Meta:
        model = Review
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    reviews = ReviewUserSerializer(many=True)

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
    avg_rating = serializers.ReadOnlyField(source='avg_rating')

    class Meta:
        model = Menu
        exclude = ('rating_sum', 'rating_count')


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


# Dish create or update for Administer
