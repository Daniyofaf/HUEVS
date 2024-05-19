from django.urls import path
from . import views

# from .views import submit_nomination  # Corrected import statement

urlpatterns = [
    path('', views.dashboard, name="board_member_dashboard"),

    # path('dashboard/', views.dashboard, name='Dashboard'),  # Updated the name to match the template
    
    path('nominationposts/', views.nominationposts, name='nominationposts'),  # Updated the name to match the template
   
    path('electionposts/', views.electionposts, name='electionposts'),  # Updated the name to match the template
    
    path('voters/', views.view_voters_list, name='voters'),  # Updated the name to match the template
    path('NominatedCandidates/', views.viewnominatedcandidate, name='viewnominatedcandidate'),
    path('approve_nomination/<int:nominee_id>/', views.approve_nomination, name='approve_nomination'),
    # path('candidates/', views.candidates, name='viewCandidates'),  # Updated the name to match the template
    
    # * Candidate
    path('candidates/', views.Candidateview, name='Candidateview'),
    path('candidates/view', views.candidate_view, name='candidate_view'),
    path('candidates/update', views.Candidatesupdate, name="updateCandidates"),
    path('candidates/delete', views.Candidatesdelete, name='deleteCandidates'),
    
    path('votes/view', views.viewVote, name='view_Vote'),
    path('votes/reset/', views.ResetVote, name='ResetVote'),
    path('votes/print/', views.PrintView.as_view(), name='printResult'),
    path('senate-member/', views.view_senate_member_by_id, name="viewSenateMembers"),
    path('result/', views.result, name='result'),
    path('board_member/announce_election/', views.announce_election, name='announce_election'),
    
    # * Position
    path('position/view', views.viewpositionbyid, name="view_Position_byid"),
    path('position/update', views.update_Position, name="update_Position"),
    path('position/delete', views.delete_Position, name='delete_Position'),
    path('positions/view', views.view_Position, name='view_Position'),

]

