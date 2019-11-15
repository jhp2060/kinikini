from django.contrib import admin
from django.urls import path, include

from .views import *

app_name ='api'

urlpatterns = [
    path('belongs_to/<int:pk>/time/<str:menu_time>/', BelongsToCafeteriaMenuDishDetailView.as_view()),
    path('cafeteria/<int:pk>/time/<str:menu_time>/', CafeteriaMenuDishDetailView.as_view()),
    path('review/create/', ReviewCreateView.as_view()),
]
