from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput
from .models import CustomUser, Contestant


class CustomAuthForm(forms.Form):
    email = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'required':'required'}))

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'required':'required'}))
    password_ = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password', 'required':'required'}))

    class Meta:
        model = CustomUser
        fields = ('name','email') 
        widgets = {
        'name':TextInput(attrs={'class':'form-control', 'placeholder':'Name', 'required':'required'}),
        'email': EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}),
    }
class ConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Confirmation Code ', 'required':'required'}))