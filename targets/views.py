from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Experience, Goal, Requirement
from instructors.models import Instructor
from .serializers import ExperienceSerializer, GoalSerializer, RequirementSerializer
# Create your views here.


def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor


class ExperienceView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = Experience.objects.filter(
                course=serializer.data['course'])
            serializer = ExperienceSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        experience = self.get_object(pk)

        if instructor == experience.instructor:
            serializer = ExperienceSerializer(experience, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = Experience.objects.filter(course=pk)
        if query.exists():
            serializer = ExperienceSerializer(query, many=True)
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        experience = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == experience.instructor:
            serializer = ExperienceSerializer(experience)
            data = serializer.data
            experience.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class GoalView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = Goal.objects.filter(course=serializer.data['course'])
            serializer = GoalSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        goal = self.get_object(pk)

        if instructor == goal.instructor:
            serializer = GoalSerializer(goal, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = Goal.objects.filter(course=pk)
        if query.exists():
            serializer = GoalSerializer(query, many=True)
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        goal = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == goal.instructor:
            serializer = GoalSerializer(goal)
            data = serializer.data
            goal.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class RequirementView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Requirement.objects.get(pk=pk)
        except Requirement.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = RequirementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = Requirement.objects.filter(
                course=serializer.data['course'])
            serializer = RequirementSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        requirement = self.get_object(pk)

        if instructor == requirement.instructor:
            serializer = RequirementSerializer(requirement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = Requirement.objects.filter(course=pk)
        if query.exists():
            serializer = RequirementSerializer(query, many=True)
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        requirement = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == requirement.instructor:
            serializer = RequirementSerializer(requirement)
            data = serializer.data
            requirement.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)
