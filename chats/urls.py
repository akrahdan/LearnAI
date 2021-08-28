from django.urls import path
from .views import ChatView, ChatUserProfileView, ChatViewDetail
urlpatterns = [
    path('compose/<slug:slug>/', ChatView.as_view()),
    path('threads/', ChatView.as_view()),
    path('threads/<int:pk>/', ChatViewDetail.as_view()),
    path('user/<int:pk>/', ChatUserProfileView.as_view()),
]