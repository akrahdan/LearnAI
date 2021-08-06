from django.urls import path
from courses.views import CreateCourseView, CourseListApiView
from .views import (
    UpdateProfileView,
    DashboardList,
    CourseList
)
urlpatterns = [
   
    path('courses/', CourseListApiView.as_view(), name='courses'),
    path('profile/', UpdateProfileView.as_view()),
    path('edit-info/', UpdateProfileView.as_view(), name='onboard'),
    path('add-course', CreateCourseView.as_view(), name='add-course'),
  
]