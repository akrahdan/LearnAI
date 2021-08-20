from django.urls import path
from .views import (
    dashboard, 
    categories, 
    course_overview, 
    category_single, 
    chats,
    instructors,
    students
)
urlpatterns = [
    path('', dashboard, name='home'),
    path('courses/', course_overview, name='courses'),
    path('categories/', categories, name='categories' ),
    path('category/', category_single, name="category"),
    path('chats/', chats, name="chats"),
    path('students/', students, name="students"),
    path('instructors/', instructors, name="instructors"),
  
]