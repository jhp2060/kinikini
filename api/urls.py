from django.contrib import admin
from django.urls import path, include, re_path

from .views import *

app_name = 'api'

urlpatterns = [
    re_path(r'^organization/<int:pk>/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})'
            r'/time/<str:menu_time>/$', OrganizationCafeteriaMenuDetailView.as_view()),
    path('review/create/', ReviewCreateView.as_view()),
    path('dish/<int:pk>/', DishDetailView.as_view()),
]
