from django.contrib import admin
from django.urls import path, include, re_path

from .views import *

app_name = 'api'

urlpatterns = [
    path('organization/<int:pk>'
         '/<int:year>/<int:month>/<int:day>'
         '/time/<str:menu_time>/', OrganizationCafeteriaMenuDetailView.as_view()),
    path('review/create/', ReviewCreateView.as_view()),
    path('dish/<int:pk>/', DishDetailView.as_view()),
]
