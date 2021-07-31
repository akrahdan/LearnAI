from rest_framework import serializers
from files.models import CourseFile
from .models import Lecture, Section


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFile
        fields = [
            'id',
            'name',
            'filetype',
            'key',
            'timestamp',
            'course'
        ]

class SectionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Section
        fields = [
            'id',
            'instructor',
            'title',
            'description',
            'course',
            'order',
            'neighbor',
            'position'
        ]

class LectureSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
 
    class Meta:
        model = Lecture
        fields = [
            'id',
            'title',
            'instructor',
            'description',
            'section',
            'video',
            'resources',
            'video_url',
            'order',
            'neighbor',
            'position'

        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['video'] = MediaSerializer(instance.video).data
        return rep



class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'id'
        ]