
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from rest_framework import authentication, permissions, serializers, status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from django.conf import settings
import vimeo
from lectures.models import Lecture, Section

from .serializers import (CreateCourseSerializer, ReviewCourseSerializer, CourseSubmitReviewSerializer,
                          CourseDetailSerializer, SearchTagsSerializer, CourseFileSerializer, CourseUpdateSerializer)
from courses.forms import CreateCourseForm, UpdateCourseForm
from .models import Course
from readux.db.models import PublishStateOptions
# Create your views here.
from .mixins import CourseMixin, AjaxFormMixin
from instructors.models import Instructor
from carts.models import Cart


def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor


class CourseDetailView(CourseMixin, DetailView):
    template_name = 'courses/detail.html'
    model = Course
    queryset = Course.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(
            *args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    # print(queryset)

class CourseListApiView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        instructor = get_instructor(request.user)
        query = Course.objects.filter(instructor = instructor)
        if query.exists():
            serializer = CourseDetailSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": 'Request forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
class CourseLevelOptions(APIView):

    def get(self, request, format=None):
        choice_values = dict(Course.CourseLevelOptions.choices)

        choices = [{'name': key, 'display': value}
                   for key, value in choice_values.items()]

        return Response(data=choices, status=status.HTTP_200_OK)


class CourseDetailApiView(RetrieveAPIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class InstructorCourseView(RetrieveAPIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseUpdateSerializer

class CourseDetailSlugView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
   
    def get_object(self, slug):
        try:
            return Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            raise Http404
    
    def get(self, request, slug, format=None):
        obj = self.get_object(slug=slug)
        serializer = CourseDetailSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CourseTagLabelView(APIView):

    def get(self, request, format=None):
        method_dict = self.request.GET
        query = method_dict.get('q', None)
        if query is not None:
            lookups = Q(tags__name__icontains=query) | Q(
                title__icontains=query)
            results = Course.objects.filter(lookups).distinct()
            serializer = SearchTagsSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Nothing"}, status=status.HTTP_204_NO_CONTENT)


class CreateCourseView(LoginRequiredMixin, AjaxFormMixin, CreateView):
    form_class = CreateCourseForm
    template_name = 'courses/add-course.html'
    success_url = 'course-create'

    def form_valid(self, form):
        obj = form.save(commit=False)
        inst, created = Instructor.objects.get_or_create(
            user=self.request.user)
        obj.instructor = inst
        obj.save()
        return super().form_valid(form)


class CreateCourseApiView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        instructor, created = Instructor.objects.get_or_create(
            user=request.user)
        serializer = CreateCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSectionView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CourseFileView(CreateAPIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseFileSerializer


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
            obj = self.get_object(pk)
            if obj.is_fully_filled():
                sections = Section.objects.filter(course=obj)
                if sections.exists():
                    if all((section.is_fully_filled for section in sections)) is False:
                        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)
                    if all([lecture.is_fully_filled() for section in sections for lecture in section.lectures.all()]) is True:

                        serializer = CourseSubmitReviewSerializer(course, data=request.data)
                        if serializer.is_valid(raise_exception=True):
                            obj = serializer.save(
                                state=PublishStateOptions.LIVE
                            )
                            obj.save()
                            return Response(serializer.data)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


class CourseEditView(APIView):
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
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
            serializer = CourseUpdateSerializer(course, data=request.data)
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
        context = super(CourseLectureDetailView,
                        self).get_context_data(*args, **kwargs)
        pk = self.kwargs.get('id')
        v = vimeo.VimeoClient(
            token=settings.VIMEO_ACCESS_TOKEN,
            key=settings.VIMEO_CLIENT_ID,
            secret=settings.VIMEO_SECRET_KEY
        )

        try:

            lecture = Lecture.objects.get(pk=pk)
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
