from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput
from .models import *

class UploadQrcodeForm(forms.Form):
    qrcode = forms.FileField()

class CreateContestForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Enter title of Contest', 'required':'required'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Simple Description of contest', 'required':'required'}))
    max_contestants = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'type':'number', 'placeholder':'Number of contestant in your contest', 'required':'required'}))

    class Meta:
        model = Contest
        fields = ['name', 'description', 'max_contestants']

class JoinContestForm(forms.Form):
    contest_code = forms.CharField(max_length=12, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Contest Code', 'required':'required'}))
    manifesto = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Why should people vote you?', 'required':'required'}))