from django.urls import path
from .import views
from account.views import account_login  # Import the account_login view from account/views.py



urlpatterns = [
    path('', views.dashboard, name="adminDashboard"),
    # * Voters
    path('voters', views.voters, name="adminViewVoters"),
    path('voters/view', views.view_voter_by_id, name="viewVoter"),
    path('voters/delete', views.deleteVoter, name='deleteVoter'),
    path('voters/update', views.updateVoter, name="updateVoter"),

    # * Position
    path('position/view', views.view_position_by_id, name="viewPosition"),
    path('position/update', views.updatePosition, name="updatePosition"),
    path('position/delete', views.deletePosition, name='deletePosition'),
    path('positions/view', views.viewPositions, name='viewPositions'),

    # Nominated Candidates
 
    path('view-nominated-candidates/', views.view_nominated_candidates, name='view_nominated_candidates'),
    path('fetch-candidate-data/', views.fetch_candidate_data, name='fetch_candidate_data'),
    path('update-candidate/', views.update_candidate, name='update_candidate'),
    path('delete-candidate/', views.delete_candidate, name='delete_candidate'),
    
        # * Candidate
    path('candidates_other/', views.Candidateviewother, name='Candidateview_other'),
    path('candidates_other/view', views.candidate_viewother, name='candidate_view_other'),
    path('candidates_other/update', views.Candidatesupdateother, name='updateCandidates_other'),
    path('candidates_other/delete', views.Candidatesdeleteother, name='deleteCandidates_other'),



    # * Settings (Ballot Position and Election Title)
    path("settings/ballot/position", views.ballot_position, name='ballot_position'),
    path("settings/ballot/title/", views.ballot_title, name='ballot_title'),
    path("settings/ballot/position/update/<int:position_id>/<str:up_or_down>/",
         views.update_ballot_position, name='update_ballot_position'),

    # * Votes
    path('votes/view', views.viewVotes, name='viewVotes'),
    path('votes/reset/', views.resetVote, name='resetVote'),
    path('votes/print/', views.PrintView.as_view(), name='printResult'),
    
    
    # * candidate account
    path('candidates-account/', views.candidate_accounts, name="adminViewCandidates"),
    path('candidates-account/view/', views.view_candidate_account_by_id, name="viewCandidate"),
    path('candidates-account/delete/', views.delete_candidate_account, name='deleteCandidates'),
    path('candidates-account/update/', views.update_candidate_account, name="updateCandidates"),
    
    
   
   # Board Members
    path('board-members/', views.board_members, name="adminViewBoardMembers"),
    path('board-members/view/', views.view_board_member_by_id, name="viewBoardMember"),
    path('board-members/update/', views.update_board_member, name="updateBoardMember"),
    path('board-members/delete/', views.delete_board_member, name="deleteBoardMember"),

    
    # Senate Members
    path('senate-members/', views.senate_members, name="adminViewSenateMembers"),
    path('senate-members/view/', views.view_senate_members_by_id, name="viewSenateMember"),
    path('senate-members/delete/', views.delete_senate_members, name='deleteSenateMember'),
    path('senate-members/update/', views.update_senate_members, name="updateSenateMember"),




]
