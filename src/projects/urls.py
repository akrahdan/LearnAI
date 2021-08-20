from django.conf.urls import include
from django.urls import path
from pricing.views import ProjectPricingView
from .views import (
ProjectListView, 
LearningOutcomeView,
HeadingView,
SyllabusView,
ProjectContentView,
ProjectView
)

urlpatterns = [
    path('', ProjectListView.as_view()),
    path('create/', ProjectView.as_view()),
    path('<int:pk>/', ProjectView.as_view()),
    path('<int:pk>/edit/', ProjectView.as_view()),
    path('syllabus/create/', SyllabusView.as_view()),
    path('<int:pk>/syllabuses/', SyllabusView.as_view()),
    path('syllabus/<int:pk>/', SyllabusView.as_view()),

    path('outcome/create/', LearningOutcomeView.as_view()),
    path('<int:pk>/outcomes/', LearningOutcomeView.as_view()),
    path('outcome/<int:pk>/', LearningOutcomeView.as_view()),


    path('heading/create/', HeadingView.as_view()),
    path('<int:pk>/heading/', HeadingView.as_view()),
    path('heading/<int:pk>/', HeadingView.as_view()),


    path('included/create/', ProjectContentView.as_view()),
    path('<int:pk>/included/', ProjectContentView.as_view()),
    path('included/<int:pk>/', ProjectContentView.as_view()),
    path('pricing/', include('pricing.urls')),
    path('<int:pk>/pricing/', ProjectPricingView.as_view()),
]