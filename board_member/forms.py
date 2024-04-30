from django import forms
from .models import NominationPost

class NominationPostForm(forms.ModelForm):
    class Meta:
        model = NominationPost
        fields = ['start_date', 'start_time', 'end_date', 'end_time']

# class ElectionPostForm(forms.ModelForm):
#     class Meta:
#         model = NominationPost
#         fields = ['start_date', 'start_time', 'end_date', 'end_time', 'Candidates']
        