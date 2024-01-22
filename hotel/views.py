from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms
from users.models import UserAccountModel


from django.contrib.auth.decorators import login_required

@login_required
def showhotel(request, category_slug = None):
    data = models.HotelModel.objects.all()
    if category_slug is not None:
        fil = models.CategoryModel.objects.get(slug=category_slug)
        data = models.HotelModel.objects.filter(category = fil)
    category = models.CategoryModel.objects.all()
    return render(request, 'hotel.html', {'data':data,'category':category})


def hotel_detail_view(request, hotel_id):
    hotel = get_object_or_404(models.HotelModel, pk=hotel_id)
    reviews = models.ReviewModel.objects.filter(hotel=hotel)

    return render(request, 'details.html', {'hotel': hotel, 'reviews': reviews,})


@login_required
def review_view(request, hotel_id):
    hotel = get_object_or_404(models.HotelModel, pk=hotel_id)
    
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user.account
            review.hotel = hotel
            review.save()
            return redirect('hotel')  
    else:
        form = forms.ReviewForm()

    return render(request, 'review.html', {'form': form, 'hotel': hotel})
 
  
class EditReviewView(UpdateView):
    model = models.ReviewModel
    form_class = forms.ReviewForm
    template_name = 'edit_review.html'
    success_url = reverse_lazy('hotel') 
    
@login_required
def delete_Review(request, id):
    record = models.ReviewModel.objects.get(pk=id)
    record.delete()
    return redirect('hotel')
