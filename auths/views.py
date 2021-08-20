import inspect
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.http.response import Http404
from allauth.account import adapter, app_settings as allauth_settings
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.views import APIView
from .serializers import ( AuthUserSerializer, UserDetailsSerializer,
 UserProfileSerializer, UserProfileDetailSerializer, UserAvatarSerializer)
from .models import UserProfile
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def get_user_profile(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        return profile
    return profile


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


class AuthLogoutView(LogoutView):
    pass
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


class UpdateUserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        if request.user is None:
            return Http404
        profile = get_user_profile(request.user)

        serializer = UserProfileDetailSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UpdateProvileView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        if request.user is None:
            return Http404
        
        profile = get_user_profile(request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user
            )
            avatar_serializer = UserAvatarSerializer(profile, context={'request': self.request})
            return Response(avatar_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    def get(self, request, format=None):
        if request.user is None:
            return Http404
        
        profile = get_user_profile(request.user)

        avatar_serializer = UserAvatarSerializer(profile, context={'request': self.request})
        return Response(avatar_serializer.data, status=status.HTTP_200_OK)



class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)




class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
        # return super().get_serializer(*args, **kwargs)
