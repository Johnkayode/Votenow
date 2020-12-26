from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput




class UploadQrcodeForm(forms.Form):
    qrcode = forms.FileField()