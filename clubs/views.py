import string

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, TemplateView



from papers.utils import process_paper_url

from .models import Candidate, Club, ClubMember, Election, Meeting, Score, Proposal, Vote
from .forms import MeetingForm, ScoreForm, ProposalForm, VoteForm
# from .utils import get_candidates_dict, get_user_clubs, get_unscored_proposals

User = get_user_model()


class HomeView(ListView):
    template_name = 'clubs/home.html'
    context_object_name = 'user_clubs'

    def get_queryset(self):
        return [x.club for x in ClubMember.objects.filter(member=self.request.user)]


class ClubDetailView(View):
    template_name = 'clubs/club-detail.html'

    def get_club(self):
        return get_object_or_404(Club, name=self.kwargs['club_name'])

    def get_context_data(self, **kwargs):
        club = self.get_club()
        ctx = club.get_ctx(self.request.user)
        if ctx['election']:
            ctx.update(**ctx['election'].get_ctx(self.request.user))
        ctx['unscored'] = list(map(lambda proposal: (proposal, ScoreForm(proposal)), ctx['unscored_proposals']))
        
        #breakpoint()
    
        return ctx

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    # TODO process forms appriorately
    def post(self, request, *args, **kwargs):
        data = request.POST
        ### Process the VoteForm if that's whats in POST
        if 'election_id' in data:
            Vote.objects.process_vote_form(request)
        ### Process the ScoreForm if that's what's in POST
        elif 'score' in data:
            Score.objects.create(user = request.user,
                                 proposal = Proposal.objects.get(pk=int(data['proposal_id'])),
                                 score = int(data['score']),
                                 club = self.get_club(),
                                 )
                                 
        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': self.get_club().name}))


class PlanMeetingView(FormView):

    form_class = MeetingForm
    # success_url = ('clubs/home')  # handled in form_valid
    template_name = 'clubs/plan-meeting.html'

    def get_club(self):
        return Club.objects.filter(name=self.kwargs['club_name']).first()
    
    def get_form_kwargs(self):
        kwargs = super(PlanMeetingView, self).get_form_kwargs()
        kwargs.update({'request': self.request,
                       'proposals': self.get_club().top_proposals,
                       })
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        election = Election.objects.create(club=self.get_club())

        for prop_id in data['selected_proposal_ids']:
            Candidate.objects.create(election=election, proposal=Proposal.objects.get(pk=int(prop_id)))

        Meeting.objects.create(club=self.get_club(),
                               leader=User.objects.get(username=data['leader']),
                               election=election,
                               date_time=data['date_time'],
                               )

        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': self.get_club().name}))


# TODO move as much of this logic and processing out of views.py
class ProposalView(FormView):

    form_class = ProposalForm
    # success_url =  # handled in 
    template_name = 'clubs/add-proposal.html'

    def get_form_kwargs(self):
        kwargs = super(ProposalView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
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
