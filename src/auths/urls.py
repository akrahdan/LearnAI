from django.urls import path
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.facebook import views as facebook_views
from .views import (AuthLoginView, 
SignupView, FacebookConnect, GoogleConnect, 
FacebookLogin, GoogleLogin )


urlpatterns = [
    path('login/', AuthLoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('facebook/connect/', FacebookConnect.as_view()),
    path('google/connect/', GoogleConnect.as_view()),
    path('google/', GoogleLogin.as_view()),
    path('facebook/', FacebookLogin.as_view()),
    path('google/url', google_views.oauth2_login),
    path('facebook/url', facebook_views.oauth2_login),
]