from django.urls import path
from django.urls.conf import include

from pricing.views import PricingView
from .views import ( CreateCourseView, CourseDetailView, CourseEditView, 
CourseSubmitReview, CourseLectureDetailView, CreateCourseApiView,
 CourseDetailApiView, CourseLevelOptions, CourseTagLabelView, CourseFileView)
from files.views import UploadCoursePolicy, DownloadCourseView
from targets.views import GoalView, RequirementView, ExperienceView
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
    

    path('<int:pk>/experience/', ExperienceView.as_view()),
    path('experience/<int:pk>/', ExperienceView.as_view()),
    path('experience/create/', ExperienceView.as_view()),

    path('<int:pk>/goals/', GoalView.as_view()),
    path('goals/<int:pk>/', GoalView.as_view()),
    path('goal/create/', GoalView.as_view()),

    path('<int:pk>/requirements/', RequirementView.as_view()),
    path('requirements/<int:pk>/', RequirementView.as_view()),
    path('requirement/create/', RequirementView.as_view()),

    path('search/', CourseTagLabelView.as_view()),
    path('section/<int:pk>/lectures/', LectureView.as_view()),
    path('section/lectures/<int:pk>/', LectureView.as_view()),
    path('lecture/create/', LectureView.as_view()),
    path('lecture/video_upload/', CourseFileView.as_view()),
    path('<int:id>/rate', submit_review, name='submit_review'),
    path('pricing/', include('pricing.urls')),
    path('<int:pk>/pricing/', PricingView.as_view())
    

]