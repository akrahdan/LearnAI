from django.urls import path
from django.contrib.auth.decorators import login_required
from billing.views import info
from .views import (
 SecurityView, terms,
 deleteProfile,
 privacy,
 socialProfile,
 security,
 linkedAccounts,
 notifications,
 ProfileEditView,
 SettingsEditView)
urlpatterns = [
    path('terms/', terms, name='account_terms'),
    path('info/', login_required(info), name='account_info'),
    path('security/', SecurityView.as_view(), name='account_security'),
    path('privacy/', login_required(privacy), name='account_privacy'),
    path('delete-profile/', login_required(deleteProfile), name='account_delete'),
    path('profile/', login_required(ProfileEditView.as_view()), name='account_profile'),
    path('settings/', login_required(SettingsEditView.as_view()), name='account_settings'),
    path('notifications/', login_required(notifications), name='account_notifications'),
    path('social-profile/', login_required(socialProfile), name='account_social'),
    path('linked-accounts/', login_required(linkedAccounts), name='account_linked'),
]