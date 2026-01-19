from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from .serializers import StudentListSerializer, StudentDetailSerializer

class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.prefetch_related('subjects').all()
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

class StudentDetailView(APIView):
    def get(self, request, pk):
        try:
            student = Student.objects.prefetch_related('subjects').get(pk=pk)
            serializer = StudentDetailSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class StudentReportView(APIView):
    """
    Returns students with all their subjects in a single row format
    Format: name, roll_number, group, subjects (|| separated)
    """
    def get(self, request):
        students = Student.objects.prefetch_related('subjects').all()
        data = []
        
        for student in students:
            subjects = student.subjects.all()
            subject_list = [s.name for s in subjects]
            subject_codes = [s.code for s in subjects]
            
            # Join with || separator
            subjects_display = ' || '.join(subject_list) if subject_list else '-'
            codes_display = ' || '.join(subject_codes) if subject_codes else '-'
            
            data.append({
                'id': student.id,
                'name': student.name,
                'roll_number': student.roll_number,
                'group': student.get_group_display() or '-',
                'class_name': student.class_name.name,
                'session': student.session.name,
                'subjects': subject_list,
                'subjects_display': subjects_display,
                'subject_codes': subject_codes,
                'codes_display': codes_display,
                'total_subjects': len(subject_list),
                'email': student.email,
                'phone': student.phone,
            })
        
        return Response({
            'count': len(data),
            'results': data
        })

