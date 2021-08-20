from django.urls import path
from .views import VideoViewedView, CourseVideoViews
urlpatterns = [
    path('<int:pk>/', VideoViewedView.as_view()),
    path('views/', CourseVideoViews.as_view()),
    path('<int:pk>/edit/', VideoViewedView.as_view())
]