import string

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import FormView, ListView, TemplateView

from papers.utils import process_paper_url

from .models import Club, ClubMember, Proposal
from .forms import ProposalForm, VoteForm
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
           'candidates': dict(zip(string.ascii_uppercase, [candidate for candidate in club.election.candidates.all()])),
           'unscored_proposals': get_unscored_proposals(club, user),
           'top_proposals': club.top_proposals,

           'vote_form': VoteForm(election=club.election),
           }

    
    return render(request, 'clubs/club.html', ctx)


def VoteFormView(request, club_name):

    club = Club.objects.get(name=club_name)
    form = VoteForm(election=club.election)
    ctx = {'form': form}
    # template_name = 'vote.html'
    # form_class = VoteForm
    success_url = ''

    return render(request, 'clubs/vote.html', ctx)

    # def form_valid(self, form):
    #     print('yeaaaaa\n\n\n\n\n\n\n\n')
    
class ProposalView(FormView):

    form_class = ProposalForm
    # TODO this should go back to previous page
    success_url = ('papers/home')
    template_name = 'clubs/add-proposal.html'

    def get_form_kwargs(self):
        kwargs = super(ProposalView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['clubs'] = get_user_clubs(self.request.user)
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        url = data['url']
        paper, authors = process_paper_url(url)


        Proposal.objects.create(user = self.request.user,
                                paper = paper,
                                club = Club.objects.get(name=data['club']),
                                msg = data['message']
                                )
        
        return HttpResponseRedirect(reverse('papers:paper-detail', kwargs={'pk': paper.id}))
