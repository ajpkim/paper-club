from django.urls import path

from . import views

app_name = 'clubs'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:club_name>/', views.club, name='club'),
    ]

