from django.urls import path
from .views import *
from knox import views as knox_views
from django.conf.urls import handler403  # Custom handler import
from .exceptions import custom_permission_denied_view  # import the custom view

# Assign the custom permission handler globally
handler403 = custom_permission_denied_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout-all'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/code-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('referrals/', ReferralListView.as_view(), name='referral-list'),
    path('clients/', UserListView.as_view(), name='user-list'),
    path('user-plan/', UpdateUserPlanView.as_view(), name='user-plan'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    
    path('user/update/<uuid:pk>/', PartialUpdateUserView.as_view(), name='partial-update-user'),
    path('user-detail/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
]
