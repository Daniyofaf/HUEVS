from django import forms
from .models import SenateMembers

class SenateMembersForm(forms.ModelForm):
    class Meta:
        model = SenateMembers
        fields = ['first_name', 'middle_name', 'last_name', 'id_number', 'email', 'phone_number', 'cgpa']


# from django import forms
# from .models import BoardMember

# class BoardMemberAccountForm(forms.ModelForm):
#     class Meta:
#         model = BoardMember
#         fields = ['username', 'password', 'email', 'cgpa']

