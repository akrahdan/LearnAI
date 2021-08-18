"""readux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from allauth.account.views import confirm_email
from django.conf.urls.static import static
from courses.views import CourseDetailSlugView
from projects.views import ProjectDetailView
from .views import home_page, CourseLeadView, pricing
from files.views import DownloadView, UploadPolicyView, UploadView, UploadCoursePolicy, DownloadCourseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('lead/', CourseLeadView.as_view(), name='course_signup'),
    path('pricing/', pricing, name='pricing'),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace="dashboard")),
    path('courses/', include('courses.urls')),
    path('course/<slug:slug>/', CourseDetailSlugView.as_view()),

    #path('auths/', include(('accounts.urls', 'auths'), 'auths')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('billing/', include(('billing.urls', 'billing'), 'billing')),
    path('instructors/', include(('instructors.urls', 'instructors'), 'instructors')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('upload/', UploadView.as_view()),
    path('upload/policy/', UploadPolicyView.as_view()),
    path('files/<int:id>/download/', DownloadView.as_view()),
    path('orders/', include('orders.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('auth/', include('auths.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/projects/', include('projects.urls')),
    path('projects/', include('projects.urls')),
    path('project/<slug:slug>/', ProjectDetailView.as_view()),
    path('api/categories/', include('categories.urls')),
    path('api/project_categories/', include('project_categories.urls')),
    re_path(r"^rest-auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", confirm_email,
        name="account_confirm_email"),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('cart/', include('carts.urls')),

   
]

# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
