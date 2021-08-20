from rest_framework import serializers
from .models import Experience, Goal, Requirement

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'name',
            'course',
            
        ]

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'id',
            'name',
            'course',
        ]

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = [
            'id',
            'name',
            'course',
            
        ]