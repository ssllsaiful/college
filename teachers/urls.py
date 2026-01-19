from django.urls import path, include
from . import views

urlpatterns = [
    
 
    path('list/', views.TeacherListView.as_view(), name='teacher_list'),

]
