from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models

from papers.models import Paper
from clubs.models import Club

User = get_user_model()


# class ClubManager(models.Manager):
    

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
    

class Score(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'(score) {self.score}: {self.paper}'


# Only allow ElectionProposal creation for election and proposal that share the same club
# Guess I don't NEED this if I write the logic correctly elsewhere
# class ElectionProposalManager()
    
class ElectionProposal(models.Model):
    election= models.ForeignKey(Election, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)

    def  __str__(self):
        return f'{self.election}: {self.proposal}'


class Vote(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    vote = models.IntegerField(default=1)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'(vote) {self.vote}: {self.paper}'
