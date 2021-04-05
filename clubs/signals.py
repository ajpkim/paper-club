from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Vote

User = get_user_model()
    

@receiver(post_save, sender=Vote)
def process_vote(sender, instance, created, **kwargs):
    # if ( Vote.objects.filter(election=instance.election).count() ==
    #      instance.club.members.count() ):
    election = instance.election
    if election.club.ballot_count == election.club.members.all().count():
        election.winner = election.declare_winner()
        election.save()
        instance.club.reading = instance.proposal.paper
        instance.club.save()
