from rest_framework import serializers
from .models import ChatMessage, Thread
from instructors.serializers import UserDetailsSerializer
class ChatSerializer(serializers.ModelSerializer):
    user= UserDetailsSerializer()
    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'thread',
            'user',
            'message',
            'timestamp'
        ]



class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first = UserDetailsSerializer()
    second = UserDetailsSerializer()
    messages = ChatSerializer(many=True)
    class Meta:
        model = Thread
        fields = [
            'id',
            'second',
            'first',
            'messages'
        ]
        depth = 1