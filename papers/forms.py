import re

import urllib.request as libreq
from urllib.error import HTTPError

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models

User = get_user_model()

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
    try:
        libreq.urlopen(url)
    except HTTPError:
        raise ValidationError(f'{url} is not a valid arXiv.org abstract or pdf page',
                              params={'url': url})
    

class ArxivURLForm(forms.Form):
    url = forms.URLField(max_length=50,
                         help_text="Link to an arXiv paper",
                         validators=[validate_arxiv_url]
                         )



