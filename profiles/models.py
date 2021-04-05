from django.db import models
from django.contrib.auth import get_user_model

from clubs.models import Club, ClubMember, Proposal, Score

User = get_user_model()

# class 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300)
    # clubs =
    # proposals =


    @property
    def clubs(self):
        return Club.objects.filter(clubmember__member=self.user)
    
    @property
    def unscored_proposals(self):
        res = {}
        scored_proposals = Proposal.objects.filter(score__user=self.user)
        for club in self.clubs:
            res[club.name] = club.proposals.difference(scored_proposals)
        return res
        
    
    def __str__(self):
        return f'{self.user.username} Profile'
