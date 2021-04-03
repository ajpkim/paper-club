import string

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse

User = get_user_model()

def validate_vote_or_score(number):
    low = 1
    high = 5
    if not low <= number <= high:
        raise ValidationError(
            f'"{number}" is out of the valid range."',
            params={'number': number}
            )

class VoteForm(forms.Form):
    """
    Dynamic form that generates a voting ballot based on the given election.
    """

    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.candidates = election.candidates.all()

        for i, candidate in enumerate(self.candidates, 1):
            self.fields[f'candidate_{i}'] = forms.IntegerField(label=string.ascii_uppercase[i-1],)
                                                              # help_text=candidate.paper.title)
    

class ProposalForm(forms.Form):

    pass
    
    
