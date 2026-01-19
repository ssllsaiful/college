from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student

class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        data = [{'id': s.id, 'name': s.name, 'roll_number': s.roll_number, 'class_name': s.class_name.name, 'session': s.session.name, 'email': s.email, 'phone': s.phone} for s in students]
        return Response(data)
