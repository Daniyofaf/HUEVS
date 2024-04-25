from django.urls import path
from . import views
from .views import view_voters_list  # Corrected import statement

urlpatterns = [
    path('', views.dashboard, name="board_member_dashboard"),

    path('dashboard/', views.dashboard, name='Dashboard'),  # Updated the name to match the template
    path('voters/', views.view_voters_list, name='voters'),  # Updated the name to match the template
    path('NominatedCandidates/', views.viewnominatedcandidate, name='viewnominatedcandidate'),
    path('candidates/', views.candidates, name='Candidate'),  # Updated the name to match the template
    path('votes/', views.votes, name='votes'),  # Updated the name to match the template



]

