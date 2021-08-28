from rest_framework import serializers
from .models import Instructor
from django.contrib.auth import get_user_model, authenticate



UserModel = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class UserInfoSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class AuthUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    

class InstructorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Instructor
        
        fields = [
          'id',
          'first_name',
          'last_name',
          'email',
          'headline',
          'avatar',
          'description'
        ]
    

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserDetailsSerializer()
    class Meta:
        model = Instructor
        
        fields = [
          'id',
          'first_name',
          'last_name',
          'user',
          'email',
          'headline',
          'description',
          'avatar'
        ]
    def get_user(self, obj):
      user_data = UserDetailsSerializer(obj['user'], context=self.context).data
      return user_data
    
  
class InstructorSearchSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserDetailsSerializer()
    class Meta:
        model = Instructor
        
        fields = [
          'id',
          'first_name',
          'last_name',
          'user',
          'email',
          'avatar'
        ]
   
    