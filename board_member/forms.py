from django import forms
from .models import ElectionPost, NominationPost

class NominationPostForm(forms.ModelForm):
    class Meta:
        model = NominationPost
        fields = [ 'end_date', 'end_time']
        widgets = {
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'Date','placeholder': 'YYYY-MM-DD'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time','placeholder': 'HH:MM'}),
        }

class ElectionPostForm(forms.ModelForm):
    class Meta:
        model = ElectionPost
        fields = [ 'end_date', 'end_time']
        widgets = {
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'Date','placeholder': 'YYYY-MM-DD'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time','placeholder': 'HH:MM'}),
        }