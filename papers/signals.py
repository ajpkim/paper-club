from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Author, AuthorPaper, KeyWord, KeyWordPaper, Paper

User = get_user_model()

@receiver(post_save, sender=Paper)
def process_paper(sender, instance, created, **kwargs):
    pass
