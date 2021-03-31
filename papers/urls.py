from django.urls import path

from . import views

app_name = 'papers'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.PaperDetailView.as_view(), name='paper-detail'),
    path('add/', views.AddPaperView.as_view(), name='add'),
    ]
