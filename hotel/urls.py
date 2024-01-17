from django.urls import path
from . import views

urlpatterns = [
    
   
    path('hotel/',  views.showhotel, name='hotel'),
    path('details/<int:hotel_id>/', views.hotel_detail_view, name='details'),

    path('review/<int:hotel_id>/', views.review_view, name='review'),
    path('edit/<int:pk>/', views.EditReviewView.as_view(), name='edit_review'),
    path('delete/<int:id>/', views.delete_Review, name='delete_review'),



    
]


