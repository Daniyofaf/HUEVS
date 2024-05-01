from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='voterDashboard'),
    path('electionpage/', views.electionpage, name='electionpage'),
    path('nominate/', views.nominate_candidate, name='nominate_candidate'),
    # path('confirmation/', views.confirmation, name='confirmation'),
        
    path('vote/', views.vote, name='vote'),
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
    path('ballot/vote', views.show_ballot, name='show_ballot'),
    path('ballot/vote/preview', views.preview_vote, name='preview_vote'),
    path('ballot/vote/submit', views.submit_ballot, name='submit_ballot'),
    

    
]
