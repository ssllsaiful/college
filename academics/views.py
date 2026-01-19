from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Class, Subject
from .serializers import SubjectSerializer, BulkSubjectImportSerializer

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
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class BulkSubjectImportView(APIView):
    """
    POST endpoint to bulk import subjects
    
    Expected JSON format:
    {
        "subjects": [
            {
                "name": "Physics 1st Paper",
                "code": "174",
                "group": "science",
                "category": "group"
            },
            ...
        ]
    }
    """
    def post(self, request):
        serializer = BulkSubjectImportSerializer(data=request.data)
        
        if serializer.is_valid():
            result = serializer.save()
            response_data = {
                'status': 'success',
                'message': f"Imported {result['total_created']} subjects successfully",
                'total_created': result['total_created'],
                'total_errors': result['total_errors'],
                'created_subjects': SubjectSerializer(result['created_subjects'], many=True).data,
                'errors': result['errors'] if result['errors'] else []
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Invalid data format',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
