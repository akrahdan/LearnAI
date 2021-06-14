from rest_framework import serializers


from .models import CourseFile, S3File


class S3FileSerializer(serializers.ModelSerializer):
    raw_filename = serializers.CharField(write_only=True) # forms.CharField
    class Meta:
        model = S3File
        fields = [
            'raw_filename',
            'name',
            'filetype'
        ]

class FileSerializer(serializers.ModelSerializer):
    raw_filename = serializers.CharField(write_only=True) # forms.CharField
    class Meta:
        model = CourseFile
        fields = [
            'raw_filename',
            'name',
            'filetype'
        ]