from django.contrib import admin

from .models import *

admin.site.register(BelongsTo)
admin.site.register(User)
admin.site.register(Cafeteria)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(Review)

