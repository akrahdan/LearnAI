from django.urls import path
from .views import ProjectCategoryView
urlpatterns = [
    path('', ProjectCategoryView.as_view()),
]