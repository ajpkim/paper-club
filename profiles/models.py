from django.db import models
from django.contrib.auth import get_user_model

from clubs.models import Club

User = get_user_model()

# class 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300)
    # clubs =
    # proposals =

    def __str__(self):
        return f'{self.user.username} Profile'
