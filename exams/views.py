from django.shortcuts import render
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import ExamMark, ExamType
from .serializers import (
    ExamMarkListSerializer, ExamMarkDetailSerializer,
    ExamMarkCreateUpdateSerializer
)
from students.models import Student
from academics.models import Subject, Session


class ExamMarkViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exam marks with filtering and bulk operations"""
    queryset = ExamMark.objects.prefetch_related('student', 'subject', 'session').all()
    serializer_class = ExamMarkListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ExamMarkDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ExamMarkCreateUpdateSerializer
        return ExamMarkListSerializer
    
    def get_queryset(self):
        """Filter exam marks based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by exam type
        exam_type_id = self.request.query_params.get('exam_type', None)
        if exam_type_id:
            queryset = queryset.filter(exam_type_id=exam_type_id)
        
        # Filter by subject
        subject_id = self.request.query_params.get('subject', None)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        # Filter by session
        session_id = self.request.query_params.get('session', None)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        # Filter by student group
        group = self.request.query_params.get('group', None)
        if group:
            queryset = queryset.filter(student__group=group)
        
        # Filter by student
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(exam_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(exam_date__lte=end_date)
        
        return queryset.order_by('-exam_date', 'student__roll_number')
    
    @action(detail=False, methods=['get'])
    def by_exam_type(self, request):
        """Get all exam marks for a specific exam type"""
        exam_type_id = request.query_params.get('exam_type_id', None)
        if not exam_type_id:
            return Response(
                {'error': 'exam_type_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        marks = self.get_queryset().filter(exam_type_id=exam_type_id)
        serializer = self.get_serializer(marks, many=True)
        
        try:
            exam_type = ExamType.objects.get(id=exam_type_id)
            exam_name = exam_type.name
        except ExamType.DoesNotExist:
            exam_name = 'Unknown'
        
        return Response({
            'exam_type': exam_name,
            'count': marks.count(),
            'marks': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def exam_types(self, request):
        """Get all available exam types"""
        exam_types = ExamType.objects.filter(is_active=True).values('id', 'name', 'description')
        return Response(list(exam_types))
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update marks for multiple students"""
        marks_data = request.data.get('marks', [])
        
        if not marks_data:
            return Response(
                {'error': 'marks array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = 0
        errors = []
        
        for mark_data in marks_data:
            try:
                mark_id = mark_data.get('id')
                if mark_id:
                    # Update existing
                    mark = ExamMark.objects.get(id=mark_id)
                    serializer = ExamMarkCreateUpdateSerializer(
                        mark, data=mark_data, partial=True
                    )
                else:
                    # Create new
                    serializer = ExamMarkCreateUpdateSerializer(data=mark_data)
                
                if serializer.is_valid():
                    serializer.save()
                    updated_count += 1
                else:
                    errors.append({
                        'student_id': mark_data.get('student'),
                        'errors': serializer.errors
                    })
            except ExamMark.DoesNotExist:
                errors.append({
                    'id': mark_id,
                    'error': 'ExamMark not found'
                })
        
        return Response({
            'updated': updated_count,
            'total': len(marks_data),
            'errors': errors
        }, status=status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS)
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Generate report for exam marks"""
        exam_type_id = request.query_params.get('exam_type_id', None)
        subject_id = request.query_params.get('subject', None)
        session_id = request.query_params.get('session', None)
        
        marks = self.get_queryset()
        
        if exam_type_id:
            marks = marks.filter(exam_type_id=exam_type_id)
        if subject_id:
            marks = marks.filter(subject_id=subject_id)
        if session_id:
            marks = marks.filter(session_id=session_id)
        
        # Calculate statistics
        total_records = marks.count()
        avg_total_marks = marks.filter(total_marks__isnull=False).aggregate(
            avg=models.Avg('total_marks')
        )['avg']
        avg_attendance = marks.filter(total_class__gt=0).aggregate(
            avg=models.Avg(models.F('present') * 100 / models.F('total_class'), output_field=models.FloatField())
        )['avg']
        
        # Get grade distribution
        grade_counts = marks.values('grade').annotate(count=models.Count('grade')).order_by('grade')
        
        return Response({
            'filters': {
                'exam_type_id': exam_type_id,
                'subject_id': subject_id,
                'session_id': session_id,
            },
            'statistics': {
                'total_records': total_records,
                'average_marks': round(avg_total_marks, 2) if avg_total_marks else 0,
                'average_attendance': round(avg_attendance, 2) if avg_attendance else 0,
            },
            'grade_distribution': list(grade_counts),
            'marks': ExamMarkListSerializer(marks, many=True).data
        })
