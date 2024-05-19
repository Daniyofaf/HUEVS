from django import forms
from .models import SenateMembers

class SenateMembersForm(forms.ModelForm):
    class Meta:
        model = SenateMembers
        fields = ['first_name', 'middle_name', 'last_name', 'id_number', 'email', 'phone_number', 'cgpa']

    def __init__(self, *args, **kwargs):
        super(SenateMembersForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
