from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User  # Not using default
from django.core.exceptions import ValidationError
from django.core import validators

# For using the custom user model
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=200, required=False, help_text='(Optional for account recovery)')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            ]
