from .models import Club, ClubMembers

def get_user_clubs(user):
    return ClubMembers.filter(member=user)
