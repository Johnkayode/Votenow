from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name='account'
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='contest:home'), name='logout'),
    path('confirm/', views.confirm, name='confirm'),
]