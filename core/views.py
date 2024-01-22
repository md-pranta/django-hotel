from django.shortcuts import render

from django.views.generic import TemplateView
from hotel.models import HotelModel

class homeview(TemplateView):
    data = HotelModel.objects.all()
    template_name = 'index.html'