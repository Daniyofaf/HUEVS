from django.urls import path
from . import views

from .views import post_campaign_message, view_campaign_messages

urlpatterns = [
    path('', views.dashboard, name="candidatedashboard"),

    path('post/', post_campaign_message, name='post_campaign_message'),
    path('view/', view_campaign_messages, name='view_campaign_messages'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),

 # * Candidate
    path('viewcandidate/', views.view_Candidate, name='viewcandidate'),
    # path('candidateview', views.viewcandidatebyid, name='viewcandidatebyid'),
    
    path('result_page/', views.result_page, name='result_page'),

]


