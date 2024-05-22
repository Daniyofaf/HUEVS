from django import forms
from .models import ElectionPost, NominationPost

from django import forms
from .models import ElectionPost, NominationPost

class NominationPostForm(forms.ModelForm):
    class Meta:
        model = NominationPost
        fields = ['start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time', 'placeholder': 'HH:MM'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time', 'placeholder': 'HH:MM'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date should be after start date.")

        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time should be after start time when the start date and end date are the same.")

        return cleaned_data


class ElectionPostForm(forms.ModelForm):
    class Meta:
        model = ElectionPost
        fields = ['start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time', 'placeholder': 'HH:MM'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control timepicker', 'type': 'time', 'placeholder': 'HH:MM'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date should be after start date.")

        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time should be after start time when the start date and end date are the same.")

        return cleaned_data
