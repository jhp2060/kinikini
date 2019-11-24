from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

from .models import Review, Dish, Sikdan, Cafeteria, Organization


# Cafeteria List Page

class SimpleDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'avg_rating',)


class SikdanSerializer(serializers.ModelSerializer):
    # dishes = serializers.SerializerMethodField()
    dishes = SimpleDishSerializer(many=True)

    class Meta:
        model = Sikdan
        fields = '__all__'

    def get_dishes(self, instance):
        sorted_dishes = instance.dishes.all().order_by('-avg_rating')
        return SimpleDishSerializer(sorted_dishes, many=True).data


class CafeteriaSerializer(serializers.ModelSerializer):
    # sikdans = serializers.SerializerMethodField()
    sikdans = SikdanSerializer(many=True)

    class Meta:
        model = Cafeteria
        fields = '__all__'

    def get_sikdans(self, instance):
        # sorted_sikdans = instance.dishes.all().order_by('-dishes[0].avg_rating')
        sorted_sikdans = instance.dishes.all()
        sorted_sikdans = sorted_sikdans[:3]
        return SikdanSerializer(sorted_sikdans, many=True).data


class OrganizationSerializer(serializers.ModelSerializer):
    cafeterias = CafeteriaSerializer(many=True)

    class Meta:
        model = Organization
        fields = '__all__'


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

# Cafeteria Page (Sikdan List)


# Dish create or update for Administer
