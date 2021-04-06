from django.urls import path

from . import views

app_name = 'clubs'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.ClubCreateView.as_view(), name='create-club'),
    path('join/', views.ClubJoinView.as_view(), name='join-club'),
    path('<str:club_name>/', views.ClubDetailView.as_view(), name='club-detail'),
    path('<str:club_name>/plan', views.PlanMeetingView.as_view(), name='plan-meeting'),
    path('<str:club_name>/proposal/', views.ProposalView.as_view(), name='add-proposal'),

    ]

