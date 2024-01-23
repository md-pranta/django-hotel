from django.shortcuts import render

from django.views.generic import TemplateView
from hotel.models import HotelModel

def homeview(request):
    data = HotelModel.objects.all()
    return render(request, 'index.html', {'data':data})