from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from .models import Project
from courses.models import Course
from courses.serializers import CourseDetailSerializer
from .models import LearningOutCome, ProjectSection, Syllabus, TitleDescription
from instructors.serializers import InstructorSerializer
from pricing.serializers import ProjectPricingSerializer
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
    id = serializers.ReadOnlyField()
    slug = serializers.ReadOnlyField()
    pricing = ProjectPricingSerializer()
    courses = CourseDetailSerializer(many=True)
    instructor = InstructorSerializer()
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
            'state',
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
            'thumbnail_url',
            'pricing'

        ]
        depth = 1

    def get_related(self, obj):
        if obj.related is not None:
            return ProjectSerializer(obj.related, many=True).data
        else:
            return None

class CreateProjectSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'category'
        ]

class ProjectCreateSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    id = serializers.ReadOnlyField()
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'goal',
            'hero',
            'experience',
            'related',
            'courses',
            'header',
            'state',
            'header_primary_color',
            'header_secondary_color',
            'video_headline',
            'difficulty',
            'progress',
            'related',
            'price',
            'tags',
            'outcomes',
            'included',
            'syllabuses',
            'thumbnail_url',
            

        ]
      

 



class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningOutCome
        fields = [
            'id',
            'title',
            'description',
            'project',
            
        ]


class SyllabusSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Syllabus
        fields = [
            'id',
            'title',
            'description',
            'project',
            
        ]

class IncludedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = TitleDescription
        fields = [
            'id',
            'title',
            'project',
            
        ]

class HeaderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = ProjectSection
        fields = [
            'id',
            'heading',
            'description',
            'projects'
            
        ]
