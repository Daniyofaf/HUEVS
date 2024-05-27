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
        
    def clean_name(self):
        first_name = self.cleaned_data['name']
        if not first_name.isalpha():
            raise forms.ValidationError("Position name should only contain letters")
        return first_name


from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo', 'video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        position = self.cleaned_data.get('position')
        
        if Candidate.objects.filter(fullname=fullname, position=position).exists():
            raise ValidationError(f"A candidate with the name {fullname} already exists for this position.")
        
        return fullname

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            max_size = 10 * 1024 * 1024  # 10 MB
            if photo.size > max_size:
                raise ValidationError("The maximum file size allowed is 10MB.")
            if not photo.content_type.startswith('image'):
                raise ValidationError("Unsupported file format. Please upload a JPEG, PNG, or GIF.")
        return photo

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            max_size = 50 * 1024 * 1024  # 50 MB
            if video.size > max_size:
                raise ValidationError("The maximum file size allowed is 50MB.")
            if not video.content_type.startswith('video'):
                raise ValidationError("Unsupported file format. Please upload an MP4, MPEG, or QuickTime video.")
        return video


class NomineeForm(FormSettings):
    class Meta:
        model = Nominee
        fields = ['fullname', 'bio']
