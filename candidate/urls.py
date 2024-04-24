from django.urls import path
from . import views

from .views import post_campaign_message, view_campaign_messages

urlpatterns = [
    path('', views.dashboard, name="candidatedashboard"),

    path('post/', post_campaign_message, name='post_campaign_message'),
    path('view/', view_campaign_messages, name='view_campaign_messages'),
]


