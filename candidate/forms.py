from django import forms
from .models import CampaignMessage

class CampaignMessageForm(forms.ModelForm):
    class Meta:
        model = CampaignMessage
        fields = ['message']
    
    def clean_message(self):
        message = self.cleaned_data['message']
        word_count = len(message.split())  # Split the message into words and count them
        if word_count < 10:
            raise forms.ValidationError("Message must contain at least 10 words.")
        return message
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
