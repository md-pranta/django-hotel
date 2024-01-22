from django.urls import path

from . import views

urlpatterns = [
    path('register/',  views.RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    path('login/',  views.Userloginviews.as_view(), name='login'),
    path('profile/<str:username>/',  views.profileview, name='profile'),
    path('deposit/', views.deposit_view, name='deposit'),

    path('booking/<int:hotel_id>/', views.hotel_booking_view, name='booking'),

    path('logout/',  views.userlogoutview.as_view(), name='logout'),
    path('passchange/',views.pass_change, name='passchange'),
]