from django.urls import path

from . import views


app_name='contest'
urlpatterns = [
    path("", views.home, name="home"),
    path('verify/', views.verify, name='verify'),
]