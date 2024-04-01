from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='voterDashboard'),
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
    path('ballot/vote', views.show_ballot, name='show_ballot'),
    path('ballot/vote/preview', views.preview_vote, name='preview_vote'),
    path('ballot/vote/submit', views.submit_ballot, name='submit_ballot'),
]
