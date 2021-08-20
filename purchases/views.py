from django.shortcuts import render
from django.views.generic import View
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

class CompletePurchaseView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(request):
        print(request.data)




