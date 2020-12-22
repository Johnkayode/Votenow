from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect

from .mail import send_confirm_mail
from .models import *
from .forms import CustomAuthForm, UserRegistrationForm, ConfirmationForm

def dashboard(request):
    if request.user.is_authenticated:
        context = {}
        return render(request,'accounts/index.html', context)
    return redirect('contest:home')


def register(request):
    
    if request.user.is_authenticated:
        return redirect('account:dashboard')  

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
       

        if user_form.is_valid():
            
            user = CustomUser.objects.filter(email=user_form.cleaned_data['email'])

            if user:
                context = {'user_form':user_form}
                messages.error(request, 'Email already exists')
                return render(request, 'accounts/register.html', context)

            else:
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.is_active = False
                new_user.save()
                '''
                try:
                    send_confirm_mail(user=new_user, email=user_form.cleaned_data['email'])
                    messages.info(request, 'A confirmation code has been sent to your address, please confirm your email address to activate your account')
                except:
                    messages.error(request, 'An error occured, try resending confirmation code')
                '''
                send_confirm_mail(user=new_user, email=user_form.cleaned_data['email'])
                messages.info(request, 'A confirmation code has been sent to your address, please confirm your email address to activate your account')
                return redirect('account:confirm')

        else:
            context = {'user_form':user_form}
            messages.error(request, 'An error occurred during registration.Try again')
            return render(request, 'accounts/register.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {'user_form':user_form}
        return render(request, 'accounts/register.html', context)

def confirm(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data('confirmation_code')
            try:
                user = CustomUser.objects.get(confirmation_code=code).first()
            except CustomUser.DoesNotExist:
                messages.error(request, 'Confirmation code is invalid')
                context = {'form':form}
                return render(request, 'accounts/confirm.html', context)
            if user.is_confirmed or user.is_active:
                messages.info(request, 'Account already confirmed')
                return redirect('account:confirm')

            user.is_confirmed = True
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been confirmed. You can log in')
            return redirect('account:login')
        else:
            messages.error(request, 'An error occured during form submission')
            context = {'form':form}
            return render(request, 'accounts/confirm.html', context)


    form = ConfirmationForm()
    context = {'form':form}
    return render(request, 'accounts/confirm.html',context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    else:
        if request.method == 'POST':
            form = CustomAuthForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, email = cd['email'], password=cd['password']) 
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'Logged in successfully')
                        return redirect('account:dashboard')
                else:
                    messages.error(request, 'Account does not exist')
        form = CustomAuthForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)