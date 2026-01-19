from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('report/', views.StudentReportView.as_view(), name='student_report'),
]
