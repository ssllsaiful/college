from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Session, Class, Subject

class SessionListView(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        data = [{'id': s.id, 'name': s.name, 'start_year': s.start_year, 'end_year': s.end_year} for s in sessions]
        return Response(data)

class ClassListView(APIView):
    def get(self, request):
        classes = Class.objects.all()
        data = [{'id': c.id, 'name': c.name, 'code': c.code} for c in classes]
        return Response(data)

class SubjectListView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        data = [{'id': s.id, 'name': s.name, 'code': s.code, 'class_name': s.class_name.name} for s in subjects]
        return Response(data)
