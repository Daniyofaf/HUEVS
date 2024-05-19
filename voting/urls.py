from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='voterDashboard'),
    path('electionpage/', views.electionpage, name='electionpage'),
    path('nominate/', views.nominate_candidate, name='nominate_candidate'),
        
    path('vote/', views.vote, name='vote'),
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
    path('ballot/vote', views.show_ballot, name='show_ballot'),
    path('ballot/vote/preview', views.preview_vote, name='preview_vote'),
    path('ballot/vote/submit', views.submit_ballot, name='submit_ballot'),
    
    path('view_ballot/', views.view_ballot, name='view_ballot'),

    path('resultpage/', views.resultpage, name='resultpage'),

    # path('candidate/platform/<int:candidate_id>/', views.candidate_platform, name='candidate_platform'),

    # path('update_candidate_bio/', views.update_candidate_bio, name='update_candidate_bio'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
