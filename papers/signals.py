from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Author, AuthorPaper, KeyWord, KeyWordPaper, Paper

User = get_user_model()

@receiver(post_save, sender=Paper)
def process_paper(sender, instance, created, **kwargs):
    pass


# TODO Listen for end of an election and turn off the candidacy flag for each of the Proposal for the election
# @receiver()
def remove_candidacy_flag(sender, instance, created, **kwargs):
    pass
    
