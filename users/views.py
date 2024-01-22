from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserAccountModel
from django.contrib.auth.models import User
from .forms import RegisterForm, DepositForm,ChangeForm

from django.views.generic import FormView, DetailView, CreateView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
# verify
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# for email
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from hotel.models import HotelModel, BookingModel
from django.contrib import messages

class RegistrationView(View):
    template_name = 'regostration.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

     
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_link = request.build_absolute_uri(activation_link)

            email_subject = 'Confirm your email'
            email_body = render_to_string('confirm_email.html', {'activation_link': activation_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return HttpResponse("Check your email for confirmation.")
        
        return render(request, self.template_name, {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)

            if user and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponse("Your account is now activated. You can log in.")
            else:
                return HttpResponse("Activation link is invalid.")
        except Exception as e:
            return HttpResponse("Activation link is invalid.")




class Userloginviews(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        if self.request.user.is_active:
            return reverse_lazy('home')
        else:
            return reverse_lazy('register')
    
class userlogoutview(View):
    def get(self, request):
        logout(request)
        return redirect('home')



@login_required
def profileview(request, username):
    visitor = get_object_or_404(UserAccountModel, user=request.user)
    
    selected_visitor = BookingModel.objects.filter(booking_man=visitor)
    user = get_object_or_404(User, username=username)
    
    data = get_object_or_404(UserAccountModel, user=user)
    
    return render(request, 'profile.html', {'data': data , 'visitor': selected_visitor})


@login_required
def deposit_view(request):
    user_account = UserAccountModel.objects.get(user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_account.balance += amount
            user_account.save()
            username = request.user.username
            messages.success(
                request,
                f' Congratulations . Successfully Deposit money')
            return redirect(reverse('profile', args=[username]))
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})



@login_required
def hotel_booking_view(request, hotel_id):
    hotel = get_object_or_404(HotelModel, pk=hotel_id)

    
    booking_man = request.user.account 
    if booking_man.balance <= hotel.fee:
        messages.warning(
            request,
            f' Your balance are less then hotel fee . Deposit money if you want to book the hotel.')

    else:
        booking_man.balance -= hotel.fee
        booking_man.save()
        messages.success(
            request,
            f' Congratulations . Successfully booking hotel')
        booking = BookingModel.objects.create(
            booking_man=booking_man,
            hotel=hotel,
        )
        email_subject = 'Booking Confirm your email'
        email_body = render_to_string('booking_mail.html', {'hotel': hotel})

        email = EmailMultiAlternatives(email_subject, '', to=[booking_man.user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        
    username = request.user.username
    return redirect(reverse('profile', args=[username]))

def pass_change(req):
    form  = PasswordChangeForm(user=req.user)
    if req.method == 'POST':
        form  = PasswordChangeForm(user = req.user, data = req.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(req, form.user)
            return redirect('profile')
    return render(req, 'passChange.html', {'form':form})
