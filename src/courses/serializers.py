from rest_framework import serializers
from .models import Course
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

import six

class CreateCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course

        fields = [
            'video_url',  
        ]




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

