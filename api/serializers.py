from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

from .models import Review, Dish, Sikdan, Cafeteria, Organization


# Review List Page & Review create Page


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# organization selection
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('organization',)


# User Drawer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'organization', 'review_cnt',)


# dish detail and review list
class ReviewUserSerializer(serializers.ModelSerializer):
    written_by = UserSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class SimpleCafeteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafeteria
        fields = ('id', 'name',)


class DishSerializer(serializers.ModelSerializer):
    cafeteria = SimpleCafeteriaSerializer()
    reviews = ReviewUserSerializer(many=True)

    class Meta:
        model = Dish
        fields = '__all__'


class DishUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name')
