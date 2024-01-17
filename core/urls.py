from django.urls import path

from . import views
urlpatterns = [
  
    path('', views.homeview.as_view(), name='home'),
]