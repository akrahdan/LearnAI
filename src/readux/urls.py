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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, course_lead, pricing
from files.views import DownloadView, UploadPolicyView, UploadView, UploadCoursePolicy, DownloadCourseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('lead/', course_lead),
    path('pricing/', pricing, name='pricing'),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace="dashboard")),
    path('courses/', include('courses.urls')),
    #path('auths/', include(('accounts.urls', 'auths'), 'auths')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('billing/', include(('billing.urls', 'billing'), 'billing')),
    path('instructors/', include(('instructors.urls', 'instructors'), 'instructors')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('upload/', UploadView.as_view()),
    path('upload/policy/', UploadPolicyView.as_view()),
    path('files/<int:id>/download/', DownloadView.as_view()),
   
]

# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
