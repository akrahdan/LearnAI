from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.


def dashboard(request):
   return render(request, 'dashboard/home_page.html')


def categories(request):
   return render(request, 'dashboard/course-category.html')

def category_single(request):
   return render(request, 'dashboard/course-category-single.html')

def course_overview(request):
   return render(request, 'dashboard/course-overview.html')

def chats(request):
   return render(request, 'dashboard/chat-app.html')

def instructors(request):
   return render(request, 'dashboard/instructor.html')

def students(request):
   return render(request, 'dashboard/students.html')