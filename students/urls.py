from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('subjects/', views.StudentSubjectListView.as_view(), name='student_subject_list'),
    path('<int:student_id>/subjects/', views.StudentSubjectByStudentView.as_view(), name='student_subjects_by_student'),
]
