from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput
from .models import *

class UploadQrcodeForm(forms.Form):
    qrcode = forms.FileField()

class CreateContestForm(forms.Form):
    name = forms.CharField(max_length=100, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Enter title of Contest', 'required':'required'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Simple Description of contest', 'required':'required'}))
    maximun_contestant = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

    class meta:
        name = Contest
        fields = ['name', 'description', 'max_contestants']
