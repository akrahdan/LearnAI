import json
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from courses.models import Course

from readux.aws.utils import AWS
from .models import CourseFile, S3File
from .serializers import FileSerializer, S3FileSerializer

User = get_user_model()

class DownloadView(View):
    def get(self, request, id, *args, **kwargs):
        file_obj = get_object_or_404(S3File, id=id)
        if request.user != file_obj.user:
            raise Http404
        url  = file_obj.get_download_url()
        return HttpResponseRedirect(url)

class UploadView(TemplateView):
    template_name = 'files/upload.html'


# Django Rest Framework -> REST API course

# @method_decorator(csrf_exempt, name='dispatch')
class UploadPolicyView(APIView): # RESTful API Endpoint
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        #print(request.body)
        data = request.data
        try:
            key             = data.get('key')
        except:
            return Response({'detail': "Invalid data"}, status=400)
        qs = S3File.objects.filter(key=key).update(uploaded=True)
        return Response({"detail": "Success!"}, status=200)


    def post(self, request, *args, **kwargs):
        """
        Requires Security
        """
        data            = request.data
        serializer      = S3FileSerializer(data=data) # ModelForm
        if serializer.is_valid(raise_exception=True):
            validated_data  = serializer.validated_data
            raw_filename    = validated_data.pop("raw_filename")
            user    = request.user
            obj     = serializer.save(
                    user=user,
                    key='/'
                )
            key     = f'users/{user.id}/files/{obj.id}/{raw_filename}'
            obj.key = key
            obj.save()
            botocfe = AWS()
            presigned_data = botocfe.presign_post_url(key=key)
            presigned_data['object_id'] = obj.id
            return Response(presigned_data)
        return Response({"detail": "Invalid request"}, status=401)




# @method_decorator(csrf_exempt, name='dispatch')
class UploadCoursePolicy(APIView): # RESTful API Endpoint
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
    
    def put(self, request, *args, **kwargs):
        #print(request.body)
        data = request.data
        try:
            key             = data.get('key')
        except:
            return Response({'detail': "Invalid data"}, status=400)
        qs = CourseFile.objects.filter(key=key).update(uploaded=True)
        return Response({"detail": "Success!"}, status=200)


    def post(self, request, *args, **kwargs):
        """
        Requires Security
        """
        print(request.data)
        course = self.get_object(pk = self.kwargs.get('id'))
        data            = request.data
        serializer      = FileSerializer(data=data) # ModelForm
        if serializer.is_valid(raise_exception=True):
            validated_data  = serializer.validated_data
            raw_filename    = validated_data.pop("raw_filename")
            
            obj     = serializer.save(
                    course=course,
                    key='/'
                )
            key     = f'media/courses/{course.id}/files/{obj.id}/{raw_filename}'
            obj.key = key
            obj.save()
            botocfe = AWS()
            presigned_data = botocfe.presign_post_url(key=key)
            presigned_data['object_id'] = obj.id
            return Response(presigned_data)
        return Response({"detail": "Invalid request"}, status=401)


class DownloadCourseView(View):
    def get(self, request, id, *args, **kwargs):
        file_obj = get_object_or_404(CourseFile, id=id)
        url  = file_obj.get_download_url()
        return HttpResponseRedirect(url)


