from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from .models import Club, ClubMember

from .utils import get_user_clubs, get_unscored_proposals

class HomeView(ListView):
    template_name = 'clubs/home.html'
    context_object_name = 'user_clubs'

    def get_queryset(self):
        return [x.club for x in ClubMember.objects.filter(member=self.request.user)]
    
class ClubView(TemplateView):

    # Need to 

    
    pass

# PLACEHOLDER VIEW
def club(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    user = request.user
    ctx = {'club': club,
           'election': club.election,
           'candidates': [candidate.proposal.paper for candidate in club.candidates],
           'unscored_proposals': get_unscored_proposals(club, user),
           'top_proposals': club.top_proposals,
           }
    print(ctx, '\n\n\n\n\n')
    return render(request, 'clubs/club.html', ctx)
