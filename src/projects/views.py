from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, ProjectCreateSerializer, OutcomeSerializer, HeaderSerializer, IncludedSerializer, SyllabusSerializer
from instructors.models import Instructor
from .models import Project, ProjectRelated, ProjectSection, LearningOutCome, Syllabus, TitleDescription
# Create your views here.
class ProjectListView(APIView):
   

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor



class ProjectView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor, created = Instructor.objects.get_or_create(
            user=request.user)
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, format=None):
        
        instructor = get_instructor(request.user)
        project = self.get_object(pk)
        if instructor == project.instructor:
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({ 'detail': 'Request denied'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        
        instructor = get_instructor(request.user)
        
        project = self.get_object(pk)
        if instructor == project.instructor:
            serializer = ProjectCreateSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)   
        return Response({ 'detail': 'Request denied'}, status=status.HTTP_400_BAD_REQUEST)
        



class HeadingView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProjectSection.objects.get(pk=pk)
        except ProjectSection.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = HeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = ProjectSection.objects.filter(
                projects__in=serializer.data['projects'])
            serializer = HeaderSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        header = self.get_object(pk)

        if instructor == header.instructor:
            serializer = HeaderSerializer(header, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = ProjectSection.objects.filter(projects__id=pk)
        if query.exists():
            serializer = HeaderSerializer(query, many=True)
            return Response(serializer.data)
        return Response({'detail:': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        header = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == header.instructor:
            serializer = HeaderSerializer(header)
            data = serializer.data
            header.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class LearningOutcomeView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return LearningOutCome.objects.get(pk=pk)
        except LearningOutCome.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = OutcomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = LearningOutCome.objects.filter(project=serializer.data['project'])
            serializer = OutcomeSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        outcome = self.get_object(pk)

        if instructor == outcome.instructor:
            serializer = OutcomeSerializer(outcome, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = LearningOutCome.objects.filter(project=pk)
        if query.exists():
            serializer = OutcomeSerializer(query, many=True)
            return Response(serializer.data)
        return Response({'detail:': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        outcome = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == outcome.instructor:
            serializer = OutcomeSerializer(outcome)
            data = serializer.data
            outcome.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class SyllabusView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Syllabus.objects.get(pk=pk)
        except Syllabus.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = SyllabusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = Syllabus.objects.filter(
                project=serializer.data['project'])
            serializer = SyllabusSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        syllabus = self.get_object(pk)

        if instructor == syllabus.instructor:
            serializer = SyllabusSerializer(syllabus, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = Syllabus.objects.filter(project=pk)
        if query.exists():
            serializer = SyllabusSerializer(query, many=True)
            return Response(serializer.data)
        return Response({'detail:': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        syllabus = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == syllabus.instructor:
            serializer = SyllabusSerializer(syllabus)
            data = serializer.data
            syllabus.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)



class ProjectContentView(APIView):
    authentication_classes = [
        SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return TitleDescription.objects.get(pk=pk)
        except TitleDescription.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)

        serializer = IncludedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            snippets = TitleDescription.objects.filter(project=serializer.data['project'])
            serializer = IncludedSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        included = self.get_object(pk)

        if instructor == included.instructor:
            serializer = IncludedSerializer(included, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = TitleDescription.objects.filter(project=pk)
        if query.exists():
            serializer = IncludedSerializer(query, many=True)
            return Response(serializer.data)
        return Response({'detail:': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        included = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == included.instructor:
            serializer = IncludedSerializer(included)
            data = serializer.data
            included.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)
