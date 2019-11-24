from django.contrib import admin

from .models import *

admin.site.register(Organization)
admin.site.register(User)
admin.site.register(Cafeteria)
admin.site.register(Sikdan)
admin.site.register(Dish)
admin.site.register(Review)

