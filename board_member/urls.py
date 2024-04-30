from django.urls import path
from . import views

# from .views import submit_nomination  # Corrected import statement

urlpatterns = [
    path('', views.dashboard, name="board_member_dashboard"),

    path('dashboard/', views.dashboard, name='Dashboard'),  # Updated the name to match the template
    
    path('nominationposts/', views.nominationposts, name='nominationposts'),  # Updated the name to match the template
   
    path('electionpost/', views.electionpost, name='electionpost'),  # Updated the name to match the template
    
    path('voters/', views.view_voters_list, name='voters'),  # Updated the name to match the template
    path('NominatedCandidates/', views.viewnominatedcandidate, name='viewnominatedcandidate'),
    path('approve_nomination/<int:nominee_id>/', views.approve_nomination, name='approve_nomination'),
    path('candidates/', views.candidates, name='Candidate'),  # Updated the name to match the template
    path('votes/', views.votes, name='votes'),  # Updated the name to match the template
    path('votes/print/', views.PrintView.as_view(), name='printResult'), 
    path('senate-member/', views.view_senate_member_by_id, name="viewSenateMembers"),

]

