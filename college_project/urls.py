"""
URL configuration for college_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include app-specific URLs
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/academics/', include('academics.urls')),
    path('api/v1/students/', include('students.urls')),
    path('api/v1/teachers/', include('teachers.urls')),
    path('api/v1/exams/', include('exams.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)