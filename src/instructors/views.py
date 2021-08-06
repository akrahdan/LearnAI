from django.http import request
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from rest_framework.response import Response
from rest_framework import status
from .models import Instructor
from rest_framework.views import APIView
from .serializers import InstructorSerializer, ProfileSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor

class UpdateProfileView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        
        instructor = get_instructor(request.user)
        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user
            )
            profile_serializer = ProfileSerializer(instructor, context={'request': self.request})
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request, format=None):

        instructor = get_instructor(request.user)
        print('Inst',instructor)
        serializer = ProfileSerializer(instructor, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
       
            

        


class DashboardList(LoginRequiredMixin,DetailView):
    template_name = 'instructors/dashboard.html'
    model = Instructor
    queryset = Instructor.objects.all()

    def get_object(self):
        user = self.request.user
        try:
            obj = Instructor.objects.get(user=user)
        
        except Instructor.DoesNotExist():
            raise Http404
        return obj


class CourseList(LoginRequiredMixin,DetailView):
    template_name = 'instructors/courses.html'
    model = Instructor
    queryset = Instructor.objects.all()

    def get_object(self):
        user = self.request.user
        try:
            obj = Instructor.objects.get(user=user)
        
        except Instructor.DoesNotExist():
            raise Http404
        return obj