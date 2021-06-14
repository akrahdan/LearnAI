from django.urls import path
from .views import CreateCourseView, CourseDetailView, CourseEditView, CourseSubmitReview, CourseLectureDetailView
from files.views import UploadCoursePolicy, DownloadCourseView
from lectures.views import CreateSectionView, CreateLectureView, upload_video, CreateVideoView
urlpatterns = [
    path('create/', CreateCourseView.as_view(), name='course-create'),
    path('<slug:slug>/', CourseDetailView.as_view() ),
    path('<slug:slug>/lecture/<int:id>/', CourseLectureDetailView.as_view(), name='current_lecture' ),
    path('<int:id>/upload_policy/', UploadCoursePolicy.as_view(), name='course_policy_upload'),
    path('<int:pk>/edit/', CourseEditView.as_view(), name='course_edit'),
    path('<int:pk>/review/', CourseSubmitReview.as_view(), name='course_review'),
    path('<int:id>/download/', DownloadCourseView.as_view()),
    path('section/create/', CreateSectionView.as_view()),
    path('lecture/create/', CreateLectureView.as_view()),
    path('lecture/video_upload/', CreateVideoView.as_view()),

]