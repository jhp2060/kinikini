from datetime import date

from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.shortcuts import render
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Organization
from .serializers import *

User = get_user_model()


class OrganizationCafeteriaMenuDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year is not None and month is not None and day is not None:
            menu_date = date(year, month, day)
        else:
            menu_date = None
        menu_time = kwargs.get('menu_time')
        if menu_time is None or menu_date is None:
            return Response(data={'error': 'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)
        organization = self.get_object()
        cafeterias = organization.cafeterias.all()
        menus = []
        for c in cafeterias:
            for menu in Menu.objects.filter(cafeteria_id=c.pk):
                if menu.time == menu_time and menu.date == menu_date:
                    menus.append(menu)
        menus = MenuSerializer(menus, many=True)
        return Response(menus.data, status=status.HTTP_200_OK)


# Review CR(U)D
class ReviewCreateView(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review = review_serializer.save()
            review.dish.rating_sum += review.rating
            review.dish.rating_count += 1
            review.dish.save()
            request.user.review_cnt += 1
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# organization selection page
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        user_serializer = UserUpdateSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for user drawer
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# for social login
class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
