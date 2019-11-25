from datetime import date

from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Organization
from .serializers import *

User = get_user_model()


class CafeteriaListView(generics.ListAPIView):
    queryset = Cafeteria.objects.all()
    # serializer_class = CafeteriaSerializer

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year is not None and month is not None and day is not None:
            sikdan_date = date(year, month, day)
        else:
            sikdan_date = None
        sikdan_time = kwargs.get('sikdan_time')
        if sikdan_time is None or sikdan_date is None:
            return Response(data={'error': 'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)
        sikdan_qs = Sikdan.objects.filter(date=sikdan_date, time=sikdan_time, organization=id)
        cafeteria_qs = Cafeteria.objects.filter(organization=id)
        results = []
        for cafeteria in cafeteria_qs:
            sikdans = []
            for sikdan in sikdan_qs.filter(cafeteria=cafeteria.id):
                main_dish = sikdan.dishes.order_by('-avg_rating').first()
                tmp = {
                    'name': main_dish.name,
                    'avg_rating': main_dish.avg_rating,
                }
                sikdans.append(tmp)
            result = {
                'id': cafeteria.id,
                'name': cafeteria.name,
                'sikdans': sorted(sikdans, key=lambda x: (x['avg_rating']), reverse=True)[:3]
            }
            results.append(result)

        return Response(results, status=status.HTTP_200_OK)


class CafeteriaDetailView(generics.RetrieveAPIView):
    queryset = Cafeteria.objects.all()
    # serializer_class = CafeteriaSerializer

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year is not None and month is not None and day is not None:
            sikdan_date = date(year, month, day)
        else: sikdan_date = None
        if sikdan_date is None:
            return Response(data={'error': 'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)
        cafeteria = self.get_object()
        queryset = Sikdan.objects.filter(date=sikdan_date,
                                         cafeteria=cafeteria)
        sikdans = []
        for sikdan in queryset:
            s = {}
            s['time'] = sikdan.time
            dishes = []
            for dish in sikdan.dishes.all():
                tmp = {
                    'id':dish.id,
                    'name': dish.name,
                    'avg_rating': dish.avg_rating,
                }
                dishes.append(tmp)
            dishes = sorted(dishes, key=lambda x: (x['avg_rating']), reverse=True)
            s['dishes'] = dishes
            sikdans.append(s)
        sikdans = sorted(sikdans, key=lambda x: (x['time']))

        result = {
            'id': cafeteria.id,
            'organization': cafeteria.organization.name,
            'name':  cafeteria.name,
            'sikdans': sikdans
        }
        return Response(data=result, status=status.HTTP_200_OK)


# Review create
class ReviewCreateView(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review = review_serializer.save()
            review.dish.rating_sum += review.rating
            review.dish.rating_count += 1
            review.dish.avg_rating \
                = review.dish.rating_sum / review.dish.rating_count
            review.dish.save()
            review.written_by.review_cnt += 1
            review.written_by.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# dish detail and review list
class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


# organization selection
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
