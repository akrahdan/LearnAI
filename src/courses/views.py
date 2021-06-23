
from django.contrib import messages
from django.http.response import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import vimeo
from lectures.models import Lecture

from .serializers import CreateCourseSerializer, ReviewCourseSerializer
from courses.forms import CreateCourseForm, UpdateCourseForm
from .models import Course
from readux.db.models import PublishStateOptions
# Create your views here.
from .mixins import CourseMixin, AjaxFormMixin
from instructors.models import Instructor
from carts.models import Cart

class CourseDetailView(CourseMixin, DetailView):
    template_name = 'courses/detail.html'
    model = Course
    queryset = Course.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    # print(queryset)

class CreateCourseView(LoginRequiredMixin, AjaxFormMixin, CreateView):
    form_class = CreateCourseForm
    template_name = 'courses/add-course.html'
    success_url = 'course-create'

    def form_valid(self, form):
        obj = form.save(commit=False)
        inst, created = Instructor.objects.get_or_create(user=self.request.user)
        obj.instructor = inst
        obj.save()
        return super().form_valid(form)
    

class CreateSectionView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class CourseSubmitReview(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        try:
            instructor = Instructor.objects.get(user=request.user)

        except Instructor.DoesNotExist:
            raise Http404
        
        if instructor == course.instructor:
            serializer = ReviewCourseSerializer(course, data=request.data)
            if serializer.is_valid(raise_exception=True):
                obj = serializer.save(
                   state = PublishStateOptions.PENDING
                )
                obj.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)
    

class CourseEditView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        try:
            instructor = Instructor.objects.get(user=request.user)

        except Instructor.DoesNotExist:
            raise Http404
        
        if instructor == course.instructor:
            serializer = CreateCourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)
  

class CourseLectureDetailView(DetailView):
    template_name = 'courses/course-active.html'
    model = Course
    queryset = Course.objects.all()
    # print(queryset)
    def get_object(self):
        kwargs = self.kwargs
        slug = kwargs.get("slug")
        try:
            return Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CourseLectureDetailView, self).get_context_data( *args, **kwargs)
        pk = self.kwargs.get('id')
        v = vimeo.VimeoClient(
                token= settings.VIMEO_ACCESS_TOKEN,
                key= settings.VIMEO_CLIENT_ID,
                secret= settings.VIMEO_SECRET_KEY
            )
        
        try:
            
            lecture = Lecture.objects.get(pk=pk )
        except Lecture.DoesNotExist:
            raise Http404("Course Does Not Exist")

        context['current_lecture'] = lecture
        return context

class CourseCheckoutView(LoginRequiredMixin, DetailView):
    template_name = 'courses/course-checkout.html'
    model = Course
    queryset = Course.objects.all()

    def get_object(self):
        kwargs = self.kwargs 
        slug = kwargs["slug"]
        try: 
            obj = Course.objects.get(slug=slug)
        except Course.DoesNotExist():
            raise Http404
        return obj




        
  

      
    
   


    

