from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Exam, Mark

class ExamListView(APIView):
    def get(self, request):
        exams = Exam.objects.all()
        data = [{'id': e.id, 'name': e.name, 'exam_type': e.exam_type, 'subject': e.subject.name, 'exam_date': e.exam_date, 'total_marks': e.total_marks} for e in exams]
        return Response(data)

class MarkListView(APIView):
    def get(self, request):
        marks = Mark.objects.all()
        data = [{'id': m.id, 'student': m.student.name, 'exam': m.exam.name, 'marks_obtained': m.marks_obtained, 'grade': m.grade, 'remarks': m.remarks} for m in marks]
        return Response(data)
