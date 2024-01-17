from django.contrib import admin

from .models import HotelModel, ReviewModel, BookingModel
# Register your models here.



admin.site.register(HotelModel)
admin.site.register(ReviewModel)
admin.site.register(BookingModel)