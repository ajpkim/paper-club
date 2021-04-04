import string

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse

from papers.forms import validate_arxiv_url
from .utils import get_user_clubs

User = get_user_model()
SCORE_OPTIONS = [(str(n), n) for n in range(1, 6)]

# Not using anymore after switch to ChoiceField
# def validate_vote_or_score(number):
#     low = 1
#     high = 5
#     if not low <= number <= high:
#         raise ValidationError(
#             f'"{number}" is out of the valid range."',
#             params={'number': number}
#             )


class VoteForm(forms.Form):
    """
    Dynamic form that generates a voting ballot based on the given election.
    """
    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.candidates = election.candidates.all()

        for i, candidate in enumerate(self.candidates, 1):
            self.fields[f'candidate_{i}'] = forms.ChoiceField(label=string.ascii_uppercase[i-1],
                                                               choices=SCORE_OPTIONS)
    #         self.fields[f'proposal_{candidate.id}'] = forms.ChoiceField(label=string.ascii_uppercase[i-1],
    #                                                           choices=self.get_choices())
    # def get_choices(self):
    #     return [(n, n) for n, candidate in enumerate(self.candidates, 1)]

class ScoreForm(forms.Form):
    """
    Form for scoring general proposals (not election candidates).
    """
    def __init__(self, proposal, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.proposal = proposal
        proposal = forms.ChoiceField(label=proposal.title,
                                     choices=SCORE_OPTIONS)


class ProposalForm(forms.Form):

    url = forms.URLField(max_length=50,
                         label="arXiv paper URL",
                         validators=[validate_arxiv_url]
                         )
    score = forms.ChoiceField(label="Score", choices=SCORE_OPTIONS)
    message = forms.CharField(max_length=300)  # TODO make this not necessary i.e. blank=True



    def __init__(self, user, clubs, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.user = user        
        self.fields['club'] = forms.ChoiceField(choices=[(club, club) for club in clubs])
        # self.fields['message'] = forms.CharField(max_length=300)
        # self.fields['score'] = forms.ChoiceField(label="Score", choices=SCORE_OPTIONS)
        # self.fields['url'] = forms.URLField(max_length=50,
        #                          label="arXiv paper URL",
        #                          validators=[validate_arxiv_url]
        #                          )

        


    
    
