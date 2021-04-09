import re

from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# class AddPaperForm(forms.ModelForm):

def validate_arxiv_url(url):
    """
    Validate the given url by ensuring it is a valid link to an arxiv.org 
    abstract page or pdf.
    """
    pat = r"^https://arxiv.org/(abs/|pdf/){1}"
    if not re.match(pat, url):
        raise ValidationError(
            f'{url} is not a valid arXiv.org abstract or pdf page',
            params={'url': url}
        )

class ArxivURLForm(forms.Form):
    url = forms.URLField(max_length=50,
                         help_text="Link to an arXiv paper",
                         validators=[validate_arxiv_url]
                         )



