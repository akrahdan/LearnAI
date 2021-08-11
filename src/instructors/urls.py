from django.urls import path
from courses.views import CreateCourseView, CourseListApiView
from .views import (
    UpdateProfileView,
    ProjectListApiView,
    DashboardList,
    CourseList
)
urlpatterns = [
   
    path('courses/', CourseListApiView.as_view(), name='courses'),
    path('projects/', ProjectListApiView.as_view()),
    path('profile/', UpdateProfileView.as_view()),
    path('edit-info/', UpdateProfileView.as_view(), name='onboard'),
    path('add-course', CreateCourseView.as_view(), name='add-course'),
  
]