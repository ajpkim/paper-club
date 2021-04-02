from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from papers.models import Paper

User = get_user_model()


class Club(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, through='ClubMember')

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.club}: {self.user}'


### Voting related models
class Proposal(models.Model):    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=300)
    total_score = models.IntegerField(default=0)
    elections = models.ManyToManyField('Election', through="ElectionProposal")

    def __str__(self):
        return f'{self.club}: {self.paper}'

    
class Election(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=(datetime.now() + timedelta(days=+2)))
    proposals = models.ManyToManyField(Proposal, through="ElectionProposal")

    def __str__(self):
        return f'(election) {self.club}'

    
class ElectionProposal(models.Model):
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
        return f'(score) {self.score}: {self.paper}'
    

class Vote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    vote = models.IntegerField(default=1)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'(vote) {self.vote}: {self.paper}'
