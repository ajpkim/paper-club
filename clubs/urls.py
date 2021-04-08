from django.urls import path

from . import views

app_name = 'clubs'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/', views.ClubCreateView.as_view(), name='create-club'),
    path('join/', views.ClubJoinView.as_view(), name='join-club'),
    path('<str:club_name>/', views.ClubDetailView.as_view(), name='club-detail'),
    path('<str:club_name>/meeting/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    path('<str:club_name>/meeting/<int:pk>/update/', views.MeetingUpdateView.as_view(), name='meeting-update'),
    path('<str:club_name>/meeting/<int:pk>/delete/', views.meeting_delete, name='meeting-delete'),
    path('<str:club_name>/plan', views.PlanMeetingView.as_view(), name='plan-meeting'),
    path('<str:club_name>/proposal/', views.ProposalView.as_view(), name='add-proposal'),
    ]

