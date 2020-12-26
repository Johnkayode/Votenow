from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .forms import PasswordChangeCustomForm


app_name='account'
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='contest:home'), name='logout'),
    path('confirm/<int:id>/', views.confirm, name='confirm'),
    path('resend-code/<int:id>/', views.resend_code, name='resend'),
    path('change-password/', auth_views.PasswordChangeView.as_view(form_class=PasswordChangeCustomForm,template_name='accounts/password_change.html', success_url=reverse_lazy('account:password_changed')), name='change_password'),
    path('change-password/done/', views.password_changed, name='password_changed'),
]