from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput
from .models import CustomUser


class CustomAuthForm(forms.Form):
    email = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'', 'required':'required'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'', 'required':'required'}))

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'', 'required':'required'}))
    password_ = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'', 'required':'required'}))

    class Meta:
        model = CustomUser
        fields = ('name','email') 
        widgets = {
        'name':TextInput(attrs={'class':'form-control', 'placeholder':'', 'required':'required'}),
        'email': EmailInput(attrs={'class':'form-control', 'placeholder':'', 'required':'required'}),
    }
    
class ConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Confirmation Code ', 'required':'required'}))

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'required':'required'}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password', 'required':'required'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm New Password', 'required':'required'}))

