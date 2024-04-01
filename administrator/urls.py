from django.urls import path
from . import views


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
    path('candidate/view', views.view_candidate_by_id, name='viewCandidate'),

    # * Settings (Ballot Position and Election Title)
    path("settings/ballot/position", views.ballot_position, name='ballot_position'),
    path("settings/ballot/title/", views.ballot_title, name='ballot_title'),
    path("settings/ballot/position/update/<int:position_id>/<str:up_or_down>/",
         views.update_ballot_position, name='update_ballot_position'),

    # * Votes
    path('votes/view', views.viewVotes, name='viewVotes'),
    path('votes/reset/', views.resetVote, name='resetVote'),
    path('votes/print/', views.PrintView.as_view(), name='printResult'),
    
    
    
    
    # path('candidates/', views.candidate_list, name='candidate_list'),

    # #candidate
    # path('register/candidate/', views.register_candidate, name='register_candidate'),
    
    # # #boardmember
    # path('register/board-member/', views.register_board_member, name='register_board_member'),


    # path('create_board_member_account/', views.create_board_member_account, name='boardMemberAccountCreate'),


    # path('board-members/create/', views.create_board_member_account, name='create_board_member_account'),
    # path('board-members/', views.board_member_list, name='board_member_list'),
    # path('board-members/<int:board_member_id>/update/', views.update_board_member, name='update_board_member'),
    # path('board-members/<int:board_member_id>/delete/', views.delete_board_member, name='delete_board_member'),


]
