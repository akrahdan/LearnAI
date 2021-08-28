
from django.http.response import Http404
from auths.models import UserProfile
from auths.serializers import UserAvatarSerializer
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Thread, ChatMessage
from .serializers import ChatSerializer, ThreadSerializer
from instructors.models import Instructor
from instructors.serializers import InstructorSearchSerializer
# Create your views here.

def get_user_profile(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        raise Http404
    return profile

def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        return None
    return instructor






class ChatUserProfileView(APIView):
    authentication_classes=[TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        instructor = get_instructor(pk)
        if instructor:
           serializer = InstructorSearchSerializer(instructor)
           return Response(serializer.data, status=status.HTTP_200_OK)

        profile = get_user_profile(pk)
        serializer = UserAvatarSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ChatView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    def create_chat_message(self, user, message):
        thread = self.chat_thread
        return ChatMessage.objects.create(thread=thread, user=user, message=message)
    
    def post(self, request, slug, format=None):
        
        thread = self.get_thread(request.user, slug)
        
        if thread:
            self.chat_thread = thread
            message = request.data.get("message", None)
           
            if message:
                obj = self.create_chat_message(request.user, message=message)
                
                qs = Thread.objects.by_user(request.user)
                
                if qs.exists():
                    seriailizers = ThreadSerializer(qs, many=True)
                    print('Thread', seriailizers.data)
                    return Response(seriailizers.data, status=status.HTTP_200_OK)
                return Response({'detail': 'No content'}, status=status.HTTP_404_NOT_FOUND)
               
            return Response({'detail:' 'Failed to create'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def get(self, request, format=None):
        if request.user:
            qs = Thread.objects.by_user(request.user)
            if qs.exists():
                seriailizers = ThreadSerializer(qs, many=True)
                return Response(seriailizers.data, status=status.HTTP_200_OK)
            return Response({'detail': 'No content'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        



class ChatViewDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try:
            obj = Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404
        return obj
        

    
    def get(self, request, pk, format=None):
        thread = self.get_object(pk)
        if request.user == thread.first or thread.second:
            serializer = ThreadSerializer(thread)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({ 'detail': 'no thread content'}, status=status.HTTP_404_NOT_FOUND)

        
        




