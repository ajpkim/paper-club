from django.urls import path

from . import views

app_name = 'papers'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('propose/', views.ProposeView.as_view(), name='propose'),
    ]
