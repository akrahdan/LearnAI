from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import UserProfile

UserModel = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', 'username')


class AuthUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserDetailsSerializer()

    def get_user(self, obj):
      user_data = UserDetailsSerializer(obj['user'], context=self.context).data
      return user_data

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = [ 'avatar']

class UserAvatarSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    class Meta:
        model = UserProfile
        fields = [ 'avatar', 'user']

    def get_user(self, obj):
      user_data = UserDetailsSerializer(obj['user'], context=self.context).data
      return user_data