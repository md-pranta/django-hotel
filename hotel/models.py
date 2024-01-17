from django.db import models
from django.contrib.auth.models import User
from users.models import UserAccountModel

# Create your models here.



class HotelModel(models.Model):
    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    fee = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='hotel/images/')

STAR_CHOICE = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class BookingModel(models.Model):
    booking_man = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelModel, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class ReviewModel(models.Model):
    reviewer = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelModel, on_delete=models.CASCADE)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    ratting = models.CharField(max_length=100, choices = STAR_CHOICE)


    def __str__(self):
        return f"{self.reviewer.user.first_name} {self.hotel.hotel_name}"


    

    