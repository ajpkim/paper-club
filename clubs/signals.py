from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Meeting, Score, Paper, Vote

User = get_user_model()
    

@receiver(post_save, sender=Vote)
def count_votes(sender, instance, created, **kwargs):
    election = instance.election
    if election.num_ballots == election.club.members.all().count():
        election.declare_winner()
        meeting = Meeting.objects.filter(election=election).first()
        meeting.paper = election.winner.paper
        meeting.save()

@receiver(post_save, sender=Score)
def add_score(sender, instance, created, **kwargs):
    instance.proposal.total_score += int(instance.score)
    instance.proposal.save()
