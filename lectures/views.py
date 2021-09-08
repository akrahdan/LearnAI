from os import stat
from django.shortcuts import render
from django.http import Http404
from django.views.generic.detail import DetailView
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings

from moviepy.editor import VideoFileClip
# Create your views here.
from rest_framework import permissions, authentication, status
from rest_framework.response import Response
from analytics.models import ObjectViewed
from files.models import CourseFile
from instructors.models import Instructor
from readux.settings.base import VIMEO_SECRET_KEY
from .models import Lecture, Section
from courses.models import Course
from .serializers import LectureSerializer, SectionSerializer, SectionCreateSerializer, MediaSerializer, ObjectViewedSerializer
from analytics.signals import object_viewed_signal
from django.contrib.contenttypes.models import ContentType
def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor


class SectionView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        section = self.get_object(pk)

        if instructor == section.instructor:
            serializer = SectionSerializer(section, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, format=None):

        instructor = get_instructor(request.user)
        query = Section.objects.filter(course=pk)
        if query.exists():
            serializer = SectionSerializer(query, many=True)
            return Response(serializer.data)
        course_qs = Course.objects.filter(id=pk)
        if course_qs.exists():
            section = Section.objects.create(
                title='Introduction', course=course_qs.first(), instructor=instructor)
            serializer = SectionSerializer(section)
            data = [serializer.data]
            return Response(data=data)

        return Response({'detail': 'Section does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):

        instructor = get_instructor(request.user)

        serializer = SectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                instructor=instructor
            )
            nb = request.data.get('neighbor', None)
            position = request.data.get('position', None)

            if nb and position:

                try:
                    obj = Section.objects.get(pk=nb)
                except Section.DoesNotExist:
                    raise Http404
                if position == 'above':
                    instance.above(obj)
                else:
                    instance.below(obj)

            snippets = Section.objects.filter(course=serializer.data['course'])
            serializer = SectionSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        section = self.get_object(pk)

        instructor = get_instructor(request.user)
        if instructor == section.instructor:
            serializer = SectionSerializer(section)
            data = serializer.data
            section.delete()
            print('Serialize: ', data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

class VideoTrackView(APIView):

    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):

        instance = self.get_object(pk)
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        view_query = ObjectViewed.objects.filter(user = request.user, content_type=content_type)
        if view_query.exists():

            serializer = ObjectViewedSerializer(view_query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK )
        return Response({ 'detail': 'No content'}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, format=None):

        
        content_type = ContentType.objects.get_for_model(Lecture)
        view_query = ObjectViewed.objects.filter(user = request.user, content_type=content_type)
        if view_query.exists():

            serializer = ObjectViewedSerializer(view_query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK )
        return Response({ 'detail': 'No content'}, status=status.HTTP_204_NO_CONTENT)

        

class LectureView(APIView):
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        query = Lecture.objects.filter(instructor=instructor)
        if query.exists():
            serializer = LectureSerializer(query, many=True)
            return Response(serializer.data)
        section_qs = Section.objects.filter(id=pk)
        if section_qs.exists():
            section = Lecture.objects.create(
                title='Introduction', section=section_qs.first(), instructor=instructor)
            serializer = LectureSerializer(section)
            data = [serializer.data]
            return Response(data=data)

        return Response({'detail': 'Section does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):

        instructor = get_instructor(request.user)
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                instructor=instructor
            )

            nb = request.data.get('neighbor', None)
            position = request.data.get('position', None)

            if nb and position:

                try:
                    obj = Lecture.objects.get(pk=nb)
                except Lecture.DoesNotExist:
                    raise Http404
                if position == 'above':
                    instance.above(obj)
                else:
                    instance.below(obj)
            lectures = Lecture.objects.filter(
                instructor=instructor)
            serializer = LectureSerializer(lectures, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instructor = get_instructor(request.user)
        lecture = self.get_object(pk)
        video_url = request.data.get("video_url", None)
        if video_url:
            clip = VideoFileClip(video_url)

        if instructor == lecture.instructor:
            serializer = LectureSerializer(lecture, data=request.data)
            if serializer.is_valid(raise_exception=True):
                obj = serializer.save()
                if clip:
                    obj.duration = clip.duration
                    obj.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        lecture = self.get_object(pk)
        instructor = get_instructor(request.user)
        if instructor == lecture.instructor:
            serializer = LectureSerializer(lecture)
            data = serializer.data
            lecture.delete()
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class MediaResourceView(APIView):
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        instructor = get_instructor(request.user)
        if course.instructor == instructor:

            files = CourseFile.objects.filter(course=course)
            if files.exists():
                serializer = MediaSerializer(files, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Not available'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk, format=None):
        course = self.get_object(pk)
        instructor = get_instructor(request.user)

        if instructor == course.instructor:
            serializer = MediaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    course=course
                )
                files = CourseFile.objects.filter(course=course)
                if files.exists():
                    serializers = MediaSerializer(files, many=True)
                    return Response(serializers.data, status=status.HTTP_201_CREATED)
                return Response({'detail': 'Not available'}, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)



