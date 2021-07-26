from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from .models import Project
from courses.models import Course


class CourseSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    url = serializers.CharField(
        source="files.last.get_download_url", read_only=True)

    class Meta:
        model = Course

        fields = [
            'id',
            'title',
            'description',
            'url',
            'tags',
        ]


class ProjectSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    thumbnail_url = serializers.CharField(
        source="files.last.get_download_url", read_only=True)
    courses = CourseSerializer(many=True)
    related = SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'lead',
            'description',
            'slug',
            'goal',
            'hero',
            'instructor',
            'experience',
            'courses',
            'completion_time',
            'related',
            'header',
            'header_primary_color',
            'header_secondary_color',
            'video_headline',
            'difficulty',
            'progress',
            'tags',
            'price',
            'outcomes',
            'included',
            'syllabuses',
            'thumbnail_url'

        ]
        depth = 1

    def get_related(self, obj):
        if obj.related is not None:
            return ProjectSerializer(obj.related, many=True).data
        else:
            return None
