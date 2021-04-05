from datetime import datetime, timedelta
from functools import reduce
import string

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone

from papers.models import Paper
from .forms import VoteForm

User = get_user_model()


class Club(models.Model):

    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User, through='ClubMember')
    reading = models.ForeignKey(Paper, null=True, blank=True, on_delete=models.SET_NULL)


    @property
    def current_reading(self):
        pass

    def get_absolute_url(self):
        return f'clubs/{self.name}/'

    @property
    def ballot_count(self):
        if self.election:
            return Vote.objects.filter(election=self.election).count() / self.election.candidates.all().count()

    def get_club_ctx(self, user):

        ctx = {'club': self,
               'election': self.election,
               'unscored_proposals': user.profile.unscored_proposals.get(self.name),
               'top_proposals': self.top_proposals,
               }
        if self.election:
            ctx['voted'] =  True if Vote.objects.filter(user=user, election=self.election).exists() else False
            ctx['candidates'] = dict(zip(string.ascii_uppercase,
                                         [c for c in self.election.candidates.all()]))
            ctx['vote_form'] = VoteForm(election=self.election)

        return ctx

    @property
    def election(self):
        """Return an active election instance or None if there isn't one"""
        election = Election.objects.filter(club=self, end_date__gte=timezone.now()).first()
        if election.is_over:
            return None
        return election  # Can also return None

    @property
    def proposals(self):
        return Proposal.objects.filter(club=self)

    @property
    def top_proposals(self):
        num = 10
        return self.proposals.order_by('total_score')[:num]

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.club}: {self.member}'


# TODO
class Meeting(models.Model):
    pass


class Proposal(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=300, null=True)
    total_score = models.IntegerField(default=0)

    def add_score(self, score):
        self.total_score += score
        self.save()

    def __str__(self):
        return f'{self.club}: {self.paper}'


class Election(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=(timezone.now() + timedelta(days=+2)))
    candidates = models.ManyToManyField(Proposal, through="Candidate", related_name="candidates")
    winner = models.ForeignKey(Proposal, null=True, blank=True, on_delete=models.SET_NULL, related_name="winner")

    @property
    def is_over(self):
        if not timezone.now() > self.end_date and not self.winner:
            return False
        return True

    def declare_winner(self):
        winner = None
        best = -1
        for candidate in self.candidates.all():
            votes = Vote.objects.filter(election=self, proposal=candidate)
            score = reduce(lambda y, x: y + x.vote, votes, 0)
            if score > best:
                winner = candidate
                best = score

        return candidate

    def __str__(self):
        return f'{self.club} Election ({self.end_date.strftime("%Y-%m-%d")})'


class Candidate(models.Model):
    election= models.ForeignKey(Election, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)

    def  __str__(self):
        return f'{self.election}: {self.proposal}'


class Score(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Score {self.score}: {self.proposal.paper}'

class VoteManager(models.Manager):

    def process_vote_form(self, request):
        data = request.POST
        n = 1
        v = []
        while ( vote_key := f"vote_{str(n)}" ) in data:
            proposal = Proposal.objects.get(pk=data[f'candidate_{n}_id'])
            election = Election.objects.get(pk=data['election_id'])
            club = Club.objects.get(name=data['club'])
            v.append(Vote.objects.create(user = request.user,
                                proposal = proposal,
                                vote = data[vote_key],
                                club = club,
                                election = election,
                                ))
            n += 1
        return v



class Vote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    vote = models.IntegerField(default=1)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    def __str__(self):
        return f'Vote {self.vote}: {self.election}: {self.proposal}'
