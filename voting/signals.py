from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Proposal, Score

User = get_user_model()

@receiver(post_save, sender=Score)
def process_score(sender, instance, created, **kwargs):
    instance.proposal.score += instance.score
    instance.propsal.save()
