from datetime import datetime, timedelta
import string

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone


from .models import Club, Meeting, Proposal

User = get_user_model()
low, high = 1, 5
SCORE_OPTIONS = [(n, n) for n in range(low, high+1)]



class ClubForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Club Name")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = Club
        fields = ['name', 'password']


class JoinClubForm(forms.Form):

    club = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        if not Club.objects.filter(name=data['club'], password=data['password']).exists():
            raise ValidationError("No Club matches that combination")


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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.club = kwargs.pop("club")
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['url'] = forms.URLField(max_length=50, label="arXiv paper URL")
        self.fields['score'] = forms.ChoiceField(label="Score", choices=SCORE_OPTIONS)
        self.fields['club'] = forms.ChoiceField(choices=[(club, club) for club in self.request.user.profile.clubs], initial=self.club)
        self.fields['message'] = forms.CharField(max_length=300)

    def clean(self):
        data = self.cleaned_data        
        if Proposal.objects.filter(Q(paper__url=data['url']) | Q(paper__pdf_url=data['url'])):
            raise ValidationError(f"A proposal for this paper already exists in {self.club}")


def validate_candidate_selection(selected_proposal_ids):
    num = 3
    if len(selected_proposal_ids) != num:
        raise ValidationError(f'Select {num} proposals')


class MeetingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.proposals = kwargs.pop("proposals")
        self.num_candidates = 3
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['leader'] = forms.CharField(widget=forms.HiddenInput(), initial=self.request.user.username)
        self.fields['date'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        self.fields['time'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        self.fields['selected_proposal_ids'] =  forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                          choices=self.get_choices(),
                                                                          label=f"Select {self.num_candidates} candidates for group election",
                                                                          validators=[validate_candidate_selection],
                                                                          )

    def get_choices(self):
        return [(x.id, x.paper) for x in self.proposals]

    # TODO check if I need to be aware of timezone info
    def clean(self):
        data = self.cleaned_data
        if datetime.now() > datetime.combine(data['date'], data['time']):
            raise ValidationError(f'Pick a future date')
        


class MeetingUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.meeting = Meeting.objects.get(pk=kwargs.pop('pk'))
        super(MeetingUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pk'] = forms.CharField(widget=forms.HiddenInput(), initial=self.meeting.id)
        self.fields['date'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                              initial=self.meeting.date_time.date())
        self.fields['time'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}),
                                              initial=self.meeting.date_time.time())
        self.fields['leader'] = forms.CharField(initial=self.meeting.leader)

    def clean(self):
        data = self.cleaned_data

        if ( not User.objects.filter(username=data['leader']).exists() or
             User.objects.get(username=data['leader']) not in self.meeting.club.members.all() ):
             raise ValidationError('Invalid meeting leader')
         
        if datetime.now() > datetime.combine(data['date'], data['time']):
            raise ValidationError(f'Pick a future date')
