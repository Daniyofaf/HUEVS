# from django import forms
# from .models import BoardMember

# class BoardMemberAccountForm(forms.ModelForm):
#     class Meta:
#         model = BoardMember
#         fields = ['username', 'password', 'email', 'cgpa', 'face_data', 'finger_data']


from django import forms
from .models import BoardMember

class BoardMemberAccountForm(forms.ModelForm):
    class Meta:
        model = BoardMember
        fields = ['username', 'password', 'email', 'cgpa']
