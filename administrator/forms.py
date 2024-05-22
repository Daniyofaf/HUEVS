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

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters")
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data['middle_name']
        if middle_name and not middle_name.isalpha():
            raise forms.ValidationError("Middle name must contain only letters")
        return middle_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long")
        if not phone_number.startswith(('07', '09')):
            raise forms.ValidationError("Phone number must start with 07 or 09")
        return phone_number

    def clean_cgpa(self):
        cgpa = self.cleaned_data['cgpa']
        if cgpa < 0 or cgpa > 4.0:
            raise forms.ValidationError("CGPA must be between 0.0 and 4.0")
        return cgpa
    
    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if not id_number.replace('/', '').isdigit():
            raise forms.ValidationError("ID number must contain only positive numbers and '/'")
        return id_number