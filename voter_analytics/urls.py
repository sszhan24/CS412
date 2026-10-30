#urls.py
#Sion Zhan (sszhan24@bu.edu), 10/27/26
#URL configurations for voter_analytics application

from django.urls import path
from . import views

app_name = 'voter_analytics'

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.VoterGraphView.as_view(), name='graphs'),
]