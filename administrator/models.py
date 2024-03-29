# from django.db import models

# # Create your models here.
# from django.shortcuts import render, redirect
# from .forms import BoardMemberForm
# from .models import BoardMemberAccountForm

# def board_member_list(request):
#     board_members = BoardMemberAccountForm.objects.all()
#     return render(request, 'administrator/board_member_list.html', {'board_members': board_members})

# def create_board_member(request):
#     if request.method == 'POST':
#         form = BoardMemberAccountForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('board_member_list')
#     else:
#         form = BoardMemberAccountForm()
#     return render(request, 'administrator/create_board_member_account.html', {'form': form})



from django.db import models

class BoardMember (models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    cgpa = models.FloatField()
    face_data = models.CharField(max_length=100)
    # finger_data = models.CharField(max_length=100)
