from django.urls import path
from .views import ( CreateCourseView, CourseDetailView, CourseEditView, 
CourseSubmitReview, CourseLectureDetailView, CreateCourseApiView,
 CourseDetailApiView, CourseLevelOptions, CourseTagLabelView, CourseFileView)
from files.views import UploadCoursePolicy, DownloadCourseView
from lectures.views import SectionView, LectureView, upload_video, CreateVideoView, MediaResourceView
from reviews.views import submit_review

urlpatterns = [
    path('create/', CreateCourseApiView.as_view(), name='course-create'),
    # path('<slug:slug>/', CourseDetailView.as_view() ),
    path('<int:pk>/', CourseDetailApiView.as_view() ),
    path('level/', CourseLevelOptions.as_view() ),
    path('<slug:slug>/lecture/<int:id>/', CourseLectureDetailView.as_view(), name='current_lecture' ),
    path('<int:id>/upload_policy/', UploadCoursePolicy.as_view(), name='course_policy_upload'),
    path('<int:pk>/edit/', CourseEditView.as_view(), name='course_edit'),
    path('<int:pk>/review/', CourseSubmitReview.as_view(), name='course_review'),
    path('<int:pk>/sections/', SectionView.as_view()),
    path('<int:pk>/resources/', MediaResourceView.as_view()),
    path('sections/<int:pk>/', SectionView.as_view()),
    path('<int:id>/download/', DownloadCourseView.as_view()),
    path('section/create/', SectionView.as_view()),
    path('search/', CourseTagLabelView.as_view()),
    path('section/<int:pk>/lectures/', LectureView.as_view()),
    path('section/lectures/<int:pk>/', LectureView.as_view()),
    path('lecture/create/', LectureView.as_view()),
    path('lecture/video_upload/', CourseFileView.as_view()),
    path('<int:id>/rate', submit_review, name='submit_review')

]