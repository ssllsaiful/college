from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'marks', views.ExamMarkViewSet, basename='exammark')

urlpatterns = [
    path('list/', views.ExamListView.as_view(), name='exam_list'),
    path('marks-legacy/', views.MarkListView.as_view(), name='mark_list'),
    path('', include(router.urls)),
]
