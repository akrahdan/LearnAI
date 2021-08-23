from django.urls import path
from courses.views import CreateCourseView, CourseListApiView, InstructorCourseView
from .views import (
    UpdateProfileView,
    ProjectListApiView,
    DashboardList,
    CourseList
)

from projects.views import InstructorProjectView
urlpatterns = [
   
    path('courses/', CourseListApiView.as_view(), name='courses'),
    path('courses/<int:pk>/', InstructorCourseView.as_view()),
  
    path('projects/', ProjectListApiView.as_view()),
    path('projects/<int:pk>/', InstructorProjectView.as_view()),
    path('profile/', UpdateProfileView.as_view()),
    path('edit-info/', UpdateProfileView.as_view(), name='onboard'),
    path('add-course/', CreateCourseView.as_view(), name='add-course'),
  
]