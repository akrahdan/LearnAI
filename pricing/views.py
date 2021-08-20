from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from projects.models import Project
from .models import Pricing, ProjectPricing, PricingTierOptions, CurrencyOptions
from .serializers import PricingSerializer, ProjectPricingSerializer
from instructors.models import Instructor
from courses.models import Course


def get_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)

    except Instructor.DoesNotExist:
        raise Http404
    return instructor


class PricingTierView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        choice_values = dict(PricingTierOptions.choices)

        choices = [{'name': key, 'display': value}
                   for key, value in choice_values.items()]
        return Response(data=choices, status=status.HTTP_200_OK)


class CurrencyOptionsView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        choice_values = dict(CurrencyOptions.choices)
        choices = [{'name': key, 'display': value}
                   for key, value in choice_values.items()]
        return Response(data=choices, status=status.HTTP_200_OK)


class PricingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)
        serializer = PricingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk, format=None):

        instructor = get_instructor(request.user)
        course = self.get_object(pk)

        if instructor == course.instructor:
            pricingQ = Pricing.objects.filter(course=course)
            if pricingQ.exists():
                obj = pricingQ.first()
                serializer = PricingSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Request data not available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Request not allowed'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):

        instructor = get_instructor(request.user)
        course = self.get_object(pk)

        if instructor == course.instructor:
            pricingQ = Pricing.objects.filter(course=course)
            if pricingQ.exists():
                obj = pricingQ.first()
                serializer = PricingSerializer(obj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            return Response({'detail': 'Request data not available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Request not allowed'}, status=status.HTTP_403_FORBIDDEN)


class ProjectPricingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        instructor = get_instructor(request.user)
        serializer = ProjectPricingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                instructor=instructor
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk, format=None):

        instructor = get_instructor(request.user)
        project = self.get_object(pk)

        if instructor == project.instructor:
            pricingQ = ProjectPricing.objects.filter(project=project)
            if pricingQ.exists():
                obj = pricingQ.first()
                serializer = ProjectPricingSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Request data not available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Request not allowed'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):

        instructor = get_instructor(request.user)
        project = self.get_object(pk)

        if instructor == project.instructor:
            pricingQ = ProjectPricing.objects.filter(project=project)
            if pricingQ.exists():
                obj = pricingQ.first()
                serializer = ProjectPricingSerializer(obj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            return Response({'detail': 'Request data not available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Request not allowed'}, status=status.HTTP_403_FORBIDDEN)
