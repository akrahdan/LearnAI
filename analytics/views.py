from os import stat
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
from moviepy.editor import *
from courses.models import Course
from lectures.serializers import LectureSerializer
from .models import LectureProgress
from io import BytesIO
from filestack import Client
from django.conf import settings
from lectures.models import Lecture
from .serializers import VideoViewedSerializer
# Create your views here.


class CourseVideoViews(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        views_qs = LectureProgress.objects.filter(user=request.user)
        if views_qs.exists():
            serializer = VideoViewedSerializer(views_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class VideoViewedView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    

    def make_thumbnail(self, request, url):
        client = Client(settings.FILESTACK_API)
        duration = request.data.get('progress', 0)
        duration = int(duration)
        clip = VideoFileClip(url)
        frame = clip.get_frame(duration)
        new_img = Image.fromarray(frame)
        memfile = BytesIO()
        new_img.save(memfile, 'JPEG')
        result = client.upload(file_obj=memfile)
        memfile.close()
        return result.url

    def get_object(self, pk):
        try:
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404
        return lecture

    def get(self, request, pk, format=None):
        lecture = self.get_object(pk)
        qs = LectureProgress.objects.filter(lecture=lecture, user=request.user)
        if qs.exists():
            serializer = VideoViewedSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = self.make_thumbnail(request, lecture.video_url)
        obj = LectureProgress.objects.create(
            thumbnail=url, progress=0, lecture=lecture, user=request.user)
        progressQs = LectureProgress.objects.filter(user = request.user)
        serializer = VideoViewedSerializer(progressQs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):

        try:
            obj = LectureProgress.objects.get(pk = pk)
        except LectureProgress.DoesNotExist:
            raise Http404
        
        lecture = self.get_object(obj.lecture.id)
        url = self.make_thumbnail(request, lecture.video_url)

        serializer = VideoViewedSerializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                thumbnail=url
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
