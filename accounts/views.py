from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect

from .mail import send_confirm_mail
from .models import *
from .forms import CustomAuthForm, UserRegistrationForm, ConfirmationForm


@login_required
def dashboard(request, id):
    user = CustomUser.objects.filter(id=id).first()
    if user == request.user:
        context = {'user': user}
        return render(request, 'accounts/index.html', context)
    return redirect('contest:home')

    



def register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard', id=request.user.id)  

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
                new_user.generate_qrcode()
                '''
                try:
                    send_confirm_mail(user=new_user, email=user_form.cleaned_data['email'])
                    messages.info(request, 'A confirmation code has been sent to your address, please confirm your email address to activate your account')
                except:
                    messages.error(request, 'An error occured, try resending confirmation code')
                '''
                send_confirm_mail(user=new_user, email=user_form.cleaned_data['email'])
                messages.info(request, 'A confirmation code has been sent to your address, please confirm your email address to activate your account')
                return redirect('account:confirm', id=new_user.id)

        else:
            context = {'user_form':user_form}
            messages.error(request, 'An error occurred during registration.Try again')
            return render(request, 'accounts/register.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {'user_form':user_form}
        return render(request, 'accounts/register.html', context)
    
def confirm(request, id):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['confirmation_code']
            
            user = CustomUser.objects.filter(confirmation_code=code, id=id).first()
            if user is None:
                messages.error(request, 'Confirmation code is invalid')
                context = {'form':form}
                return render(request, 'accounts/confirm.html', context)
            elif user.is_confirmed or user.is_active:
                messages.info(request, 'Account already confirmed')
                return redirect('account:confirm',id=id)
            else:
                user.is_confirmed = True
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been confirmed. You can log in')
                return redirect('account:login')
        else:
            messages.error(request, 'An error occured during form submission')
            context = {'form':form, 'id':id}
            return render(request, 'accounts/confirm.html', context)


    form = ConfirmationForm()
    print(id)
    context = {'form':form, 'id':id}
    return render(request, 'accounts/confirm.html',context)

def resend_code(request, id):
    user = CustomUser.objects.get(id=id)
    form = ConfirmationForm()
    
    if user:
        send_confirm_mail(user=user, email=user.email)
        messages.info(request, 'A confirmation code has been sent to your address, please confirm your email address to activate your account')
        return redirect('account:confirm',id=id)

def password_changed(request):
    messages.success(request, 'Password changed')
    return redirect('account:dashboard')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard', id=request.user.id)
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
                        return redirect('account:dashboard', id=user.id)
                else:
                    messages.error(request, 'Account does not exist')
        form = CustomAuthForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)


