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



# from django.db import models

# class BoardMember (models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     email = models.EmailField()
#     cgpa = models.FloatField()
#     # face_data = models.CharField(max_length=100)
#     # finger_data = models.CharField(max_length=100)




# from administrator import admin


# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at')  # Example of adding additional fields
#     search_fields = ['user__email']  # Add search functionality
#     list_filter = ('created_at',)  # Add filters
#     actions = ['mark_as_verified']  # Add custom actions

#     def mark_as_verified(self, request, queryset):
#         # Custom action logic
#         queryset.update(verified=True)
        
# from django.db import models

# class Candidate(models.Model):
#     user = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE)
    # Add other fields related to the candidate if needed

        
# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at')  # Example of adding additional fields
#     search_fields = ['user__email']  # Add search functionality
#     list_filter = ('created_at',)  # Add filters
#     actions = ['mark_as_verified']  # Add custom actions

#     def mark_as_verified(self, request, queryset):
#         # Custom action logic
#         queryset.update(verified=True)

