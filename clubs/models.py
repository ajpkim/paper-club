from datetime import datetime, timedelta
from functools import reduce
import string

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone

from papers.models import Paper


User = get_user_model()


class Club(models.Model):

    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    members = models.ManyToManyField(User, through='ClubMember')

    @property
    def meeting(self):
        """Return the current active meeting or None"""
        meeting = Meeting.objects.filter(club=self, date_time__gte=timezone.now()).last()
        if meeting and not self.election and not meeting.paper:
            # No votes in the most recent election. Need to declare a default winner and meeting paper.
            election = self.elections.last()
            election.declare_winner(election.candidates.first())  
            meeting.paper = election.winner.paper
            meeting.save()
        return meeting

    @property
    def election(self):
        """Return an active election instance or None if there isn't one"""
        election = Election.objects.filter(club=self, end_datetime__gte=timezone.now()).last()
        return election if election and not election.is_over else None

    @property
    def elections(self):
        return Election.objects.filter(club=self).order_by('end_datetime')

    @property
    def proposals(self):
        return Proposal.objects.filter(club=self)

    @property
    def top_proposals(self):
        num = 10
        return self.proposals.order_by('-total_score')[:num]

    def get_absolute_url(self):
        return f'clubs/{self.name}/'

    def get_ctx(self, user):
        """
        Return context dictionary for views and forms.
        """
        ctx = {'club': self,
               'meeting': self.meeting,
               'election': self.election,
               'unscored_proposals': user.profile.unscored_proposals.get(self.name),
               'top_proposals': self.top_proposals,
               }
        return ctx

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.club}: {self.member}'


class Meeting(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    election = models.ForeignKey('Election', on_delete=models.SET_NULL, null=True)
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField()

    def get_absolute_url(self):
        return f'/clubs/{self.club}/meeting/{self.id}/'

    def __str__(self):
        return f'{self.club.name} Meeting on {self.date_time.strftime("%Y-%m-%d")}'

class Proposal(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=300, null=True)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.club}: {self.paper}'


class Election(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField()
    candidates = models.ManyToManyField(Proposal, through="Candidate", related_name="candidates")
    winner = models.ForeignKey(Proposal, null=True, blank=True, on_delete=models.SET_NULL, related_name="winner")

    @property
    def is_over(self):
        """
        Return boolean representing election status. Compute winner if election
        end has passed and no winner has been declared yet.
        """
        if self.winner:
            return True
        elif timezone.now() > self.end_datetime:
            self.declare_winner()
            return True
        return False

    @property
    def num_ballots(self):
        return Vote.objects.filter(election=self).count() / self.candidates.all().count()

    @property
    def hours_left(self):
        if not self.is_over:
            return (self.end_datetime - timezone.now()).total_seconds() // 3600

    def get_ctx(self, user):
        ctx = {'voted': True if Vote.objects.filter(user=user, election=self).exists() else False,
               'candidates': dict(zip(string.ascii_uppercase,
                                      [c for c in self.candidates.all()])),
               }

        return ctx

    def declare_winner(self, proposal=None):
        winner = None or proposal
        best = -1
        for candidate in self.candidates.all():
            votes = Vote.objects.filter(election=self, proposal=candidate)
            score = reduce(lambda y, x: y + x.vote, votes, 0)
            if score > best:
                winner = candidate
                best = score
        self.winner = winner
        self.save()
        return self.winner

    def __str__(self):
        return f'{self.club} Election ({self.end_datetime.strftime("%Y-%m-%d %HH:%MM")})'


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
    submission_datetime = models.DateTimeField(auto_now_add=True)

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
    submission_datetime = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    def __str__(self):
        return f'Vote {self.vote}: {self.election}: {self.proposal}'
