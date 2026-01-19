from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from students.models import Student
from teachers.models import Teacher
from exams.models import Exam
from academics.models import Class, Session

class DashboardView(APIView):
    def get(self, request):
        data = {
            'total_students': Student.objects.count(),
            'total_teachers': Teacher.objects.count(),
            'total_exams': Exam.objects.count(),
            'total_classes': Class.objects.count(),
            'total_sessions': Session.objects.count(),
        }
        return Response(data)
