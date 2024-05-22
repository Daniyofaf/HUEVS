import re
from django import forms
from .models import *
from django.contrib.auth.hashers import make_password


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


# class CustomUserForm(FormSettings):
#     email = forms.EmailField(required=True)
#     # email = forms.EmailField(required=True)
#     password = forms.CharField(widget=forms.PasswordInput)

#     widget = {
#         'password': forms.PasswordInput(),
#     }


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    id_number = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    # face_id = models.IntegerField()

    
    # live_camera_photo = forms.ImageField(required=False)
    # finger_data = forms.CharField(required=False, widget=forms.HiddenInput)
    
    


    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
        else:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")
        return formEmail

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if self.instance.pk is not None:
            if not password:
                # return None
                return self.instance.password

        return make_password(password)


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("First name should only contain letters")
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data['middle_name']
        if not middle_name.isalpha():
            raise forms.ValidationError("Middle name should only contain letters")
        return middle_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain letters")
        return last_name

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if not re.match(r'^\d{4}/\d{2}$', id_number):
            raise forms.ValidationError("ID number must be in the format XXXX/YY")
        return id_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'^0[79]\d{8}$', phone_number):
            raise forms.ValidationError("Phone number must start with 09 or 07 and be 10 digits long")
        return phone_number
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'id_number', 'email', 'password', 'phone_number'] # , 'live_camera_photo' , 'finger_data'



class BoardMemberForm(FormSettings):
    class Meta:
        model = BoardMember
        fields = ['phone_number', 'email']
        
        
class AdminCandidateCreationform(FormSettings):
    class Meta:
        model = AdminCandidateCreation
        fields = ['phone_number', 'email']
        