from django import forms
from .models import NominationPost

class NominationPostForm(forms.ModelForm):
    class Meta:
        model = NominationPost
        fields = ['start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker','type':'Date', 'placeholder': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time','placeholder': 'HH:MM'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type':'Date','placeholder': 'YYYY-MM-DD'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type':'time','placeholder': 'HH:MM'}),
        }
