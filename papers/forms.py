from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# class AddPaperForm(forms.ModelForm):

def validate_arxiv(url):
    if not url.startswith('https://arxiv.org/'): # and not url.startswith('http://arxiv.org/'):
        raise ValidationError(
            f'"{url}" is not an arXiv.org link',
            params={'url': url}
            )

class ArxivURLForm(forms.Form):
    url = forms.URLField(max_length=50, help_text="Link to an arXiv paper", validators=[validate_arxiv])



