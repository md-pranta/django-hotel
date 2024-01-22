# django builtin model forom
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from .models import UserAccountModel


GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female')
)
class RegisterForm(UserCreationForm):
    
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    
    class Meta:
        model = User
        
        fields = ['username', 'first_name', 'last_name', 'email', 'gender']
        
    def save(self, commit= True):
        user =  super().save(commit=False)
        if commit == True:
            user.is_active = False
            user.save() 
             
        
            UserAccountModel.objects.create(
                user = user,
                account_no = 1000000 + user.id,
                balance = 100,
                gender = self.cleaned_data['gender']
            )
            
        return user



class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1.00)

class ChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
