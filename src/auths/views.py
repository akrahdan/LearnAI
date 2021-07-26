import inspect
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.http.response import Http404
from allauth.account import adapter, app_settings as allauth_settings
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialConnectView, SocialLoginView
from .serializers import AuthUserSerializer, UserDetailsSerializer

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AuthLoginView(LoginView):

    def get_response_serializer(self):
        response_serializer = AuthUserSerializer
        return response_serializer

    def get_response(self):

        data = {
            'user': self.user,
            'token': self.token
        }
        serializer_class = self.get_response_serializer()
        tokenSerializer = serializer_class(
            instance=data, context={'request': self.request})

        response = Response(data=tokenSerializer.data)
        return response


class SignupView(RegisterView):

    def get_response_data(self, user):

        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        data = {
            'user': user,
            'token': user.auth_token
        }
        return AuthUserSerializer(instance=data, context={'request': self.request}).data

        

class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client