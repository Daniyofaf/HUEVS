from django import forms
from .models import CampaignMessage

class CampaignMessageForm(forms.ModelForm):
    class Meta:
        model = CampaignMessage
        fields = ['message']
