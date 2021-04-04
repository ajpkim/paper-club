import string

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, TemplateView


from papers.utils import process_paper_url

from .models import Club, ClubMember, Score, Proposal
from .forms import ProposalForm, VoteForm
from .utils import get_candidates_dict, get_user_clubs, get_unscored_proposals



class HomeView(ListView):
    template_name = 'clubs/home.html'
    context_object_name = 'user_clubs'

    def get_queryset(self):
        return [x.club for x in ClubMember.objects.filter(member=self.request.user)]
    

class ClubDetailView(View):
    template_name = 'clubs/club-detail.html'
    
    def get_object(self):
        return get_object_or_404(Club, name=self.kwargs['club_name'])

    def get_context_data(self, **kwargs):
        club = self.get_object()
        user = self.request.user
        ctx = {'club': club,
               'election': club.election,
               'unscored_proposals': get_unscored_proposals(club, user),
               'top_proposals': club.top_proposals,
               }
    
        if club.election:
            ctx['candidates'] = get_candidates_dict(club)
            ctx['vote_form'] = VoteForm(election=club.election)

        return ctx

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    # TODO process forms appriorately
    def post(self, request, *args, **kwargs):
        breakpoint()
        print(f'POSTING FORM!!!\n\n{request}')
        pass
    

# TODO try using a VoteFormView and ScoreFormView to handle
# posting of vote/score data in club-detail pages
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


# TODO move as much of this logic and processing out of views.py
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
        user = self.request.user
        club = Club.objects.get(name=data['club'])
        msg = data['message']
        paper, authors = process_paper_url(url)

        if not Proposal.objects.filter(paper=paper, club=club).exists():
            
            proposal = Proposal.objects.create(user = user,
                                    paper = paper,
                                    club = club,
                                    msg = msg
                                    )

            Score.objects.create(user=user,
                                 proposal=proposal,
                                 score=data['score'],
                                 club=club,
                                 )

            return HttpResponseRedirect(reverse('clubs:club-detail', kwargs={'club_name': club.name}))

        else:

            # TODO add a message about proposal duplication

            return HttpResponseRedirect(reverse('clubs:club-detail', kwargs={'club_name': club.name}))
