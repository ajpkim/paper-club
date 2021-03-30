from django.urls import include, path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='pages-home'),
    path('about/', views.AboutView.as_view(), name='pages-about'),
]
