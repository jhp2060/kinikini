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


class CafeteriaListView(generics.ListAPIView):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer

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
        sikdans = Sikdan.objects.filter(date=sikdan_date, time=sikdan_date,
                                       organization=id)
        data = CafeteriaSerializer(sikdans=sikdans).data
        return Response(data, status=status.HTTP_200_OK)


class CafeteriaDetailView(generics.RetrieveAPIView):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer

    def get(self, request, *args, **kwargs):
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
        cafeteria = self.get_object()
        sikdans = cafeteria.sikdans.filter(date=sikdan_date,
                                                 time=sikdan_time)

        # data = CafeteriaSerializer(sikdans=sikdans, many=True).data
        ss = SikdanSerializer(sikdans, many=True)
        return Response(ss.data, status=status.HTTP_200_OK)

class sss(generics.RetrieveAPIView):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer

# class OrganizationSikdanDetailView(generics.RetrieveAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#
#     def get(self, request, *args, **kwargs):
#         year = kwargs.get('year')
#         month = kwargs.get('month')
#         day = kwargs.get('day')
#         if year is not None and month is not None and day is not None:
#             sikdan_date = date(year, month, day)
#         else:
#             sikdan_date = None
#         sikdan_time = kwargs.get('sikdan_time')
#         if sikdan_time is None or sikdan_date is None:
#             return Response(data={'error': 'url invalid'},
#                             status=status.HTTP_404_NOT_FOUND)
#         organization = self.get_object()
#         cafeterias = organization.cafeterias.all()
#         cs = []
#         for c in cafeterias:
#             ss = []
#             for sikdan in c.sikdans.all():
#                 if sikdan.date == sikdan_date and sikdan.time == sikdan_time:
#                     ss.append(sikdan)
#             ss = SikdanSerializer(ss, many=True)
#             cs.append(ss)
#         cafeterias = CafeteriaSerializer(cs, many=True)
#         return Response(cafeterias.data, status=status.HTTP_200_OK)


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
