from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ExamListView.as_view(), name='exam_list'),
    path('marks/', views.MarkListView.as_view(), name='mark_list'),
]
