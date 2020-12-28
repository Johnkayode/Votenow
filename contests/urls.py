from django.urls import path

from . import views


app_name='contest'
urlpatterns = [
    path("", views.home, name="home"),
    path('verify/', views.verify, name='verify'),
    path('create_contest/', views.contest, name='create-contest'),
    path('join_contest/', views.join_contest, name='join-contest')
]