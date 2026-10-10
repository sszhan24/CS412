#urls.py
#Sion Zhan (sszhan24@bu.edu), 9/24/2026
#Description: url patterns/configuration for mini insta app.
#Maps url patterns to views

from django.urls import path
from . import views

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('feed/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/create_post', views.CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name='update_post'),
]