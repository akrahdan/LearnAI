from django.shortcuts import render
from django.http import Http404
from django.views.generic.detail import DetailView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings
import vimeo
# Create your views here.
from rest_framework import permissions, authentication, status
from rest_framework.response import Response

from readux.settings.base import VIMEO_SECRET_KEY
from .models import Lecture, Section
from .serializers import LectureSerializer, SectionSerializer, VideoSerializer

class CreateSectionView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = Section.objects.all()
        serializer = SectionSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user
            )
            snippets = Section.objects.filter(course = serializer.data['course'])
            serializer = SectionSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateLectureView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = Lecture.objects.all()
        serializer = LectureSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user= request.user
            )
            snippets = Lecture.objects.filter(section = serializer.data['section'])
            serializer = LectureSerializer(snippets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateVideoView(APIView):

    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def post(self, request, format=None):

        lectureId = request.POST.get('id')
        lecture = self.get_object(lectureId)
        if lecture.user == request.user:

            tempFile = request.FILES.get('file')
            file = tempFile.temporary_file_path()
            v = vimeo.VimeoClient(
                token= settings.VIMEO_ACCESS_TOKEN,
                key= settings.VIMEO_CLIENT_ID,
                secret= settings.VIMEO_SECRET_KEY
            )
            video_url = v.upload(file,
            data= {'name': lecture.title, 'description': lecture.description})
            lecture.video_url = video_url
            lecture.save()
            return HttpResponse('courses/lecture/video_upload')
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

def upload_video(request):
    if request.method == "POST":
        print(request.POST.get('id'))
        tempFile = request.FILES.get('file')
        file = tempFile.temporary_file_path()
        v = vimeo.VimeoClient(
            token= settings.VIMEO_ACCESS_TOKEN,
            key= settings.VIMEO_CLIENT_ID,
            secret= settings.VIMEO_SECRET_KEY
        )
        video_url = v.upload(file)
    print(video_url)
    return HttpResponse('courses/lecture/video_upload')



    
