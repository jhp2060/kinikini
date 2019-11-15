from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import BelongsTo
from .serializers import *


class BelongsToCafeteriaMenuDishDetailView(generics.RetrieveAPIView):
    queryset = BelongsTo.objects.all()
    serializer_class = BelongsToSerializer

    def get(self, request, *args, **kwargs):
        menu_time = kwargs.get('menu_time')
        if menu_time is None:
            return Response(data={'error':'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)
        belongs_to = self.get_object()
        cafeterias = belongs_to.cafeterias.all()

        menu = cafeterias.get


class CafeteriaMenuDishDetailView(generics.RetrieveAPIView):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer

    def get(self, request, *args, **kwargs):
        menu_time = kwargs.get('menu_time')
        if menu_time is None:
            return Response(data={'error': 'url invalid'},
                            status=status.HTTP_404_NOT_FOUND)
        cafeteria = self.get_object()
        menus = cafeteria.menus.filter(time=menu_time)
        ms = MenuSerializer(menus, many=True)
        return Response(ms.data, status=status.HTTP_200_OK)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    # serializer_class = ReviewSerializer

    # def post(self, request, *args, **kwargs):
    #     review_serializer = ReviewSerializer(data=request.data)
    #
    #     if review_serializer.is_valid():
    #         new_review = review_serializer.save()
    #         user_pk = request.POST.get('written_by', None)
    #
    #     else :
    #         return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)






