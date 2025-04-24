from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/account/', views.UserUpdateView.as_view(), name='account_update'),

    # Password management
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),

    # User management
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.user_detail, name='user_detail'),

    # Follow system
    path('users/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('users/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('users/<str:username>/following/', views.following_list, name='following_list'),
    path('following/posts/', views.following_posts, name='following_posts'),
]
