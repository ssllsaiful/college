from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/bulk-import/', views.BulkSubjectImportView.as_view(), name='subject_bulk_import'),
]
