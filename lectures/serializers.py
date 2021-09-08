from rest_framework import serializers
from files.models import CourseFile
from .models import Lecture, Section
from django.db.models import Sum
from django.db.models.functions import Round
from analytics.models import ObjectViewed
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
            'duration',
            'video_url',
            'order',
            'neighbor',
            'position'

        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['video'] = MediaSerializer(instance.video).data
        return rep

class SectionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    lectures = LectureSerializer(many=True)
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
            'position',
            'lectures'
        ]
        read_only_fields = ['lectures']


class SectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    lectures = LectureSerializer(many=True)
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
            'position',
          
        ]
       
class ObjectViewedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectViewed
        fields = [
            'object_id'
        ]



class SectionPlayerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    duration = serializers.SerializerMethodField()
    lectures = LectureSerializer(many=True)
    class Meta:
        model = Section
        fields = [
            'id',
            'instructor',
            'title',
            'duration',
            'description',
            'course',
            'order',
            'neighbor',
            'lectures',
            'position'
        ]
    def get_duration(self, instance):
        avg = instance.lectures.aggregate(Sum("duration"))
        return avg["duration__sum"]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'id'
        ]