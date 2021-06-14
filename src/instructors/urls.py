from django.urls import path
from courses.views import CreateCourseView
from .views import (
    dashboard,
    reviews,
    payouts,
    earnings,
    students,
    orders,
    courses,
    addCourse
)
urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('reviews', reviews, name='reviews'),
    path('payouts', payouts, name='payouts'),
    path('students', students, name='students'),
    path('earnings', earnings, name='earnings'),
    path('orders', orders, name='orders'),
    path('courses', courses, name='courses'),
    path('add-course', CreateCourseView.as_view(), name='add-course'),
  
]