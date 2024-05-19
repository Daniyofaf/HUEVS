from django import forms
from .models import *
from account.forms import FormSettings


class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['phone_number']


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'id_number', 'bio', 'position', 'photo', 'video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }

class NomineeForm(FormSettings):
    class Meta:
        model = Nominee
        fields = ['fullname', 'bio']
