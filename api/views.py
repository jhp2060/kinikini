from datetime import date

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Organization
from .serializers import *


class OrganizationCafeteriaMenuDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year is not None and month is not None and day is not None:
            menu_date = date(int(year), int(month), int(day))
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
                if menu.time is menu_time and menu.date is menu_date:
                    menus.append(menu)
        menus = MenuSerializer(menus, many=True)
        return Response(menus.data, status=status.HTTP_200_OK)


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
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
