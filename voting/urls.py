from django.urls import path

from . import views

app_name = 'voting'
urlpatterns = [
    path('', views.home, name='home'),
    ]
