import json
from datetime import date

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

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
        else:
            sikdan_date = None
        sikdan_time = kwargs.get('sikdan_time')
        if sikdan_time is None or sikdan_date is None:
            return Response(data={'error': 'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)

        cafeteria = self.get_object()
        queryset = Sikdan.objects.filter(date=sikdan_date,
                                         cafeteria=cafeteria,
                                         time=sikdan_time)
        sikdans = []
        for sikdan in queryset:
            s = {}
            bap = {}
            kimchi = {}
            dishes = []
            for dish in sikdan.dishes.all():
                if "쌀밥" in dish.name or "잡곡밥" in dish.name \
                    or "차조밥" in dish.name or "기장밥" in dish.name \
                    or "콩밥" in dish.name or "공기밥" in dish.name \
                    or "공깃밥" in dish.name or "흑미밥" in dish.name\
                        or "귀리밥" in dish.name or "차조밥" in dish.name:
                    bap = {
                        'id': dish.id,
                        'name': dish.name,
                        'avg_rating': dish.avg_rating,
                    }
                    continue
                elif "김치" == dish.name[-2:] or "단무지" in dish.name \
                    or "깍두기" in dish.name or "피클" in dish.name \
                    or "석박지" in dish.name:
                    kimchi = {
                        'id': dish.id,
                        'name': dish.name,
                        'avg_rating': dish.avg_rating,
                    }
                    continue
                tmp = {
                    'id': dish.id,
                    'name': dish.name,
                    'avg_rating': dish.avg_rating,
                }
                dishes.append(tmp)
            dishes = sorted(dishes, key=lambda x: (x['avg_rating']), reverse=True)
            if kimchi != {} : dishes.insert(0, kimchi)
            if bap != {}: dishes.insert(0, bap)
            s['dishes'] = dishes
            sikdans.append(s)

        result = {
            'id': cafeteria.id,
            'organization': cafeteria.organization.name,
            'name': cafeteria.name,
            'sikdans': sikdans,
        }
        return Response(data=result, status=status.HTTP_200_OK)


# Review create
class ReviewCreateView(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        # f = open("./log.txt", mode='w', encoding='utf-8')
        # f.write("request.data : " + str(request.data) + "\n")
        request_str = list(dict(request.data.lists()).keys())[0]
        review_serializer = ReviewSerializer(data=json.loads(request_str))
        if review_serializer.is_valid():
            review = review_serializer.save()
            review.dish.rating_sum += review.rating
            if review.rating == 1:
                review.dish.pt1_cnt += 1
            elif review.rating == 2:
                review.dish.pt2_cnt += 1
            elif review.rating == 3:
                review.dish.pt3_cnt += 1
            elif review.rating == 4:
                review.dish.pt4_cnt += 1
            elif review.rating == 5:
                review.dish.pt5_cnt += 1
            review.dish.rating_count += 1
            review.dish.avg_rating = review.dish.rating_sum / review.dish.rating_count
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


