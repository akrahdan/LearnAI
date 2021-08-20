from rest_framework import serializers
from .models import LectureProgress


class VideoViewedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    class Meta:
        model = LectureProgress
        fields = [
            'progress',
            'id',
            'lecture',
            'thumbnail',
            'updated',
            'complete', 
        ]

   
class CurrentVideoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    course = serializers.ReadOnlyField()
    class Meta:
        model = LectureProgress
        fields = [
            'progress',
            'course',
            'id',
            'lecture',
            'thumbnail',
            
        ]

   
