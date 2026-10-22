#urls.py
#Sion Zhan (sszhan24@bu.edu), 9/24/2026
#Description: url patterns/configuration for mini insta app.
#Maps url patterns to views

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('feed/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('profile/create_post', views.CreatePostView.as_view(), name='create_post'),
    path('profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', views.ShowFeedView.as_view(), name='show_feed'),
    path('profile/search', views.SearchView.as_view(), name='search'),
    path('profile', views.MyProfileView.as_view(), name='my_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:logout_confirmation'), name='logout'),
    path('logout-confirmation/', views.LogoutConfirmationView.as_view(), name='logout_confirmation'),
]