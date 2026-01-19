from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, StudentSubject
from .serializers import StudentListSerializer, StudentDetailSerializer, StudentSubjectSerializer

class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

class StudentDetailView(APIView):
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentDetailSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class StudentSubjectListView(APIView):
    def get(self, request):
        student_subjects = StudentSubject.objects.select_related('student', 'subject').all()
        serializer = StudentSubjectSerializer(student_subjects, many=True)
        return Response(serializer.data)

class StudentSubjectByStudentView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(pk=student_id)
            student_subjects = student.student_subjects.all()
            serializer = StudentSubjectSerializer(student_subjects, many=True)
            return Response({
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'roll_number': student.roll_number,
                    'class_name': student.class_name.name,
                },
                'subjects': serializer.data,
                'total_subjects': student_subjects.count()
            })
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class StudentSubjectReportView(APIView):
    """
    Returns students with all their subjects in a single row format
    Format: name, roll_number, group, subjects (comma-separated)
    """
    def get(self, request):
        students = Student.objects.prefetch_related('student_subjects__subject').all()
        data = []
        
        for student in students:
            student_subjects = student.student_subjects.all()
            
            # Get all groups
            groups = list(set([ss.group for ss in student_subjects if ss.group]))
            
            # Get all subjects
            subject_list = [ss.subject.name for ss in student_subjects]
            
            # Get subject codes
            subject_codes = [ss.subject.code for ss in student_subjects]
            
            data.append({
                'id': student.id,
                'name': student.name,
                'roll_number': student.roll_number,
                'class_name': student.class_name.name,
                'session': student.session.name,
                'group': ', '.join(groups) if groups else '-',
                'subjects': subject_list,
                'subject_codes': subject_codes,
                'total_subjects': len(subject_list),
                'email': student.email,
                'phone': student.phone,
            })
        
        return Response({
            'count': len(data),
            'results': data
        })

