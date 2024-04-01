# from django.contrib import admin
# from .models import Candidate

# @admin.register(Candidate)
# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at')  # Assuming 'created_at' is a valid field of the Candidate model
#     search_fields = ['user__email']
#     actions = ['mark_as_verified']

#     def mark_as_verified(self, request, queryset):
#         queryset.update(verified=True)
