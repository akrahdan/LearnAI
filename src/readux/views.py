from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def home_page(request):
    return render(request, 'home_page.html', {})

def course_lead(request):
    return render(request, 'course_lead.html', {})

def pricing(request):
    return render(request, 'pricing.html', {})