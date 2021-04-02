from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
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


