from datetime import timedelta
import string

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils import timezone

from papers.forms import validate_arxiv_url


User = get_user_model()
low, high = 1, 5
SCORE_OPTIONS = [(n, n) for n in range(low, high+1)]

class VoteForm(forms.Form):
    """
    Dynamic form that generates a voting ballot based on the given election.
    """
    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.candidates = election.candidates.all()

        for i, candidate in enumerate(self.candidates, 1):
            self.fields[f'vote_{i}'] = forms.ChoiceField(label=string.ascii_uppercase[i-1], choices=SCORE_OPTIONS)
            self.fields[f'candidate_{i}_id'] = forms.CharField(widget=forms.HiddenInput(), initial=candidate.id)

        self.fields['election_id'] = forms.CharField(widget=forms.HiddenInput(), initial=election.id)
        self.fields['club'] = forms.CharField(widget=forms.HiddenInput(), initial=election.club.name)


class ScoreForm(forms.Form):
    """
    Form for scoring new proposals (not election candidates).
    """
    def __init__(self, proposal, *args, **kwargs):
        self.proposal = proposal
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['score'] = forms.ChoiceField(choices=SCORE_OPTIONS, label="")
        self.fields['proposal_id'] = forms.CharField(widget=forms.HiddenInput(), initial=self.proposal.id)


class ProposalForm(forms.Form):

    url = forms.URLField(max_length=50,
                         label="arXiv paper URL",
                         validators=[validate_arxiv_url]
                         )
    score = forms.ChoiceField(label="Score", choices=SCORE_OPTIONS)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':3})) # TODO make this not necessary i.e. blank=True

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['club'] = forms.ChoiceField(choices=[(club, club) for club in self.request.user.profile.clubs])

        # self.fields['message'] = forms.CharField(max_length=300)
        # self.fields['score'] = forms.ChoiceField(label="Score", choices=SCORE_OPTIONS)
        # self.fields['url'] = forms.URLField(max_length=50,
        #                          label="arXiv paper URL",
        #                          validators=[validate_arxiv_url]
        #                          )


# TODO validate datetime in future

# def validate_meeting_date(date):
#     if date < (timezone.now() + timedelta(days=+1)).date():
#         raise ValidationError(f'Pick a later date')

def validate_candidate_selection(selected_proposal_ids):
    num = 3
    if len(selected_proposal_ids) != num:
        raise ValidationError(f'Select {num} proposals')


class MeetingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.proposals = kwargs.pop("proposals")
        super(MeetingForm, self).__init__(*args, **kwargs)

        # TODO Reduce to singel DateTime field
        self.fields['leader'] = forms.CharField(widget=forms.HiddenInput(), initial=self.request.user.username)
        self.fields['date_time'] = forms.DateTimeField()
        # self.fields['date'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        #                                       validators=[validate_meeting_date],
        #                                       )

        # self.fields['time'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        self.fields['selected_proposal_ids'] =  forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                          choices=self.get_choices(),
                                                                          label="Select candidates for group election",
                                                                          validators=[validate_candidate_selection],
                                                                          )

    def get_choices(self):
        return [(x.id, x.paper) for x in self.proposals]
