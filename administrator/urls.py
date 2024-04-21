from django.urls import path
from . import views
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

    # * Candidate
    path('candidate/', views.viewCandidates, name='viewCandidates'),
    path('candidate/update', views.updateCandidate, name="updateCandidate"),
    path('candidate/delete', views.deleteCandidate, name='deleteCandidate'),
    path('candidate/view', views.view_candidate_by_id, name='view_candidate_by_id'),

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
    path('candidate_dashboard/', views.candidate_dashboard, name="CandidateDashboard"),

    path('candidates', views.candidatesaccount, name="adminViewCandidates"),
    path('candidates/view', views.view_candidates_by_id, name="viewCandidate"),
    path('candidates/delete', views.delete_candidates, name='deleteCandidates'),
    path('candidates/update', views.update_candidates, name="updateCandidates"),
    
    
   
   # Board Members
    path('board-members/', views.board_members, name="adminViewBoardMembers"),
    path('board-members/view/', views.view_board_member_by_id, name="viewBoardMember"),
    path('board-members/delete/', views.delete_board_member, name='deleteBoardMember'),
    path('board-members/update/', views.update_board_member, name="updateBoardMember"),
    
    
    
#  # * Board Member account
#     path('board_member_dashboard/', views.board_member_dashboard, name="BoardMemberDashboard"),
 
#     path('board_members/', views.board_members_account, name='board_members_account'),
#     path('board_members/view/', views.view_board_member_by_id, name='view_board_member'),
#     path('board_members/delete/', views.delete_board_member, name='delete_board_member'),
#     path('board_members/update/', views.update_board_member, name='update_board_member'),

#     # path('create_board_member/', views.create_board_member, name='create_board_member'),





]
