from django.http import request
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .forms import InstructorForm
from .models import Instructor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
def dashboard(request):
    return render(request, 'instructors/dashboard.html')

def reviews(request):
    return render(request, 'instructors/reviews.html')

def earnings(request):
    return render(request, 'instructors/earning.html')

def students(request):
    return render(request, 'instructors/students.html')

def payouts(request):
    return render(request, 'instructors/payouts.html')

def orders(request):
    return render(request, 'instructors/order.html')

def courses(request):
    return render(request, 'instructors/courses.html')

def addCourse(request):
    return render(request, 'courses/add-course.html')

class CreateInstructorProfile(LoginRequiredMixin,CreateView):
    template_name = 'instructors/create_form.html'
    model = Instructor
    form_class = InstructorForm
    success_url = reverse_lazy('instructors:dashboard')

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        obj.user = user
        obj.save()
        return super().form_valid(form)

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