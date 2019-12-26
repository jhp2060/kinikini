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
    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self,obj):
        return obj.written_at.timestamp() * 1000

    class Meta:
        model = Review
        exclude = ('written_at',)


class SimpleCafeteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafeteria
        fields = ('id', 'name',)


class DishSerializer(serializers.ModelSerializer):
    cafeteria = SimpleCafeteriaSerializer()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'

    def get_reviews(self, instance):
        reviews = instance.reviews.all().order_by('-written_at')
        return ReviewUserSerializer(reviews,many=True).data


class DishUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name',  'cafeteria', 'avg_rating',)


class SikdanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sikdan
        fields = ('time', 'date','organization','cafeteria')