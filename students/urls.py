from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
]
