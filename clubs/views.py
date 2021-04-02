from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from .models import Club, ClubMember

class HomeView(ListView):
    template_name = 'clubs/home.html'
    context_object_name = 'user_clubs'
    # user_clubs = UserClub.objects.get(username=User)

    def get_queryset(self):
        user = self.request.user
        user_clubs = [x.club for x in ClubMember.objects.filter(user=user)]
        return user_clubs

    
class ClubView(TemplateView):

    # Need to 

    
    pass
    
def club(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    ctx = {'club': club,}
    return render(request, 'clubs/club.html', ctx)
