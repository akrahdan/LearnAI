from rest_framework import serializers

from .models import Lecture, Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'id',
            'title',
            'description',
            'course'
        ]

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'id',
            'title',
            'description',
            'section',

        ]
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'id'
        ]