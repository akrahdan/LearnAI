from rest_framework import serializers
from .models import Course
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

import six

class CreateVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course

        fields = [
            'video_url',  
        ]


class CreateCourseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'category',
            'description',
            
        ]

class LevelOptionsSerializer(serializers.Serializer):
    levels = serializers.MultipleChoiceField(Course.CourseLevelOptions.choices)

class CourseDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'category',
            'description',
            'level'
        ]
        depth = 2
       
class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)
        return value

class ReviewCourseSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Course
        exclude = [
            'title'
        ]
    

class SearchTagsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Course
        fields = [
            'title',
            'tags'
        ]

