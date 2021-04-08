import string

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from papers.utils import process_paper_url
from .models import Candidate, Club, ClubMember, Election, Meeting, Score, Proposal, Vote
from .forms import ClubForm, JoinClubForm, MeetingForm, MeetingUpdateForm, ScoreForm, ProposalForm, VoteForm


User = get_user_model()


class HomeView(ListView):
    template_name = 'clubs/home.html'
    context_object_name = 'user_clubs'

    def get_queryset(self):
        return [x.club for x in ClubMember.objects.filter(member=self.request.user)]
    

class ClubCreateView(CreateView):
    form_class = ClubForm
    model = Club

    def form_valid(self, form):
        data = form.cleaned_data
        club = Club.objects.create(name=data['name'])
        ClubMember.objects.create(member=self.request.user, club=club, password=data['password'])
        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': club.name}))

    
class ClubJoinView(FormView):
    form_class = JoinClubForm
    template_name = 'clubs/join-club.html'
    success_url = 'clubs/home'

    def form_valid(self, form):
        data = form.cleaned_data
        club = Club.objects.get(name=data['club'])
        if self.request.user not in club.members.all():
            ClubMember.objects.create(club=club, member=self.request.user)
        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': club.name}))
        

class ClubDetailView(View):
    template_name = 'clubs/club-detail.html'

    def get_club(self):
        return get_object_or_404(Club, name=self.kwargs['club_name'])

    def get_context_data(self, **kwargs):
        club = self.get_club()
        ctx = club.get_ctx(self.request.user)
        if ctx['election']:
            ctx.update(**ctx['election'].get_ctx(self.request.user))
            if not ctx['voted']:
                ctx['vote_form'] = VoteForm(election=ctx['election'])
                ctx['voteform_fields_candidates_zip'] = list(zip(ctx['election'].candidates.all(),
                                                                 ctx['vote_form'].visible_fields()))
        if ctx['unscored_proposals']:
            ctx['unscored'] = list(map(lambda proposal: (proposal, ScoreForm(proposal)), ctx['unscored_proposals']))

        return ctx

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = request.POST
        # Process a VoteForm
        if 'election_id' in data:
            Vote.objects.process_vote_form(request)
        # Process a ScoreForm
        elif 'score' in data:
            Score.objects.create(user = request.user,
                                 proposal = Proposal.objects.get(pk=int(data['proposal_id'])),
                                 score = int(data['score']),
                                 club = self.get_club(),
                                 )
                                 
        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': self.get_club().name}))

# TODO 
class MeetingDetailView(DetailView):
    template_name = "clubs/meeting-detail.html"
    model = Meeting

    # def get_context_data(self, *args, **kwargs):
    #     pass
    

class PlanMeetingView(FormView):

    form_class = MeetingForm
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


# TODO This meeting update/delete process is hacky and needs to be cleaned up
class MeetingUpdateView(FormView):

    form_class = MeetingUpdateForm
    template_name = 'clubs/meeting-update.html'

    def get_form_kwargs(self):
        kwargs = super(MeetingUpdateView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs['pk']})  # self.kwargs contains club_name and pk (meeting pk)
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        meeting = Meeting.objects.get(pk=data['pk'])
        meeting.date_time = data['date_time']
        meeting.leader = User.objects.get(username=data['leader'])
        meeting.save()

        return HttpResponseRedirect(reverse("clubs:club-detail", kwargs={'club_name': meeting.club.name}))



def meeting_delete(request, *args, **kwargs):
    meeting = get_object_or_404(Meeting, pk=kwargs['pk'])
    club = meeting.club
    
    if request.method == 'POST':
        meeting.election.delete()
        meeting.delete()
        return HttpResponseRedirect(reverse('clubs:club-detail', kwargs={'club_name': meeting.club.name}))

    return HttpResponseRedirect(club.get_absolute_url())
    


    
    
    


# TODO move as much of this logic and processing out of views.py
class ProposalView(FormView):

    form_class = ProposalForm
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
