from django.contrib import admin

from .models import HotelModel, ReviewModel, BookingModel,CategoryModel
# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'slug']


admin.site.register(CategoryModel,BrandAdmin)
admin.site.register(HotelModel)
admin.site.register(ReviewModel)
admin.site.register(BookingModel)