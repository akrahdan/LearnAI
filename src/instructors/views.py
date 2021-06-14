from django.shortcuts import render

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