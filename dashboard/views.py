from django.shortcuts import render
from django.db.models import Count, Avg, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from students.models import Student
from teachers.models import Teacher
from exams.models import Exam, Mark
from academics.models import Class, Session, Subject

class DashboardView(APIView):
    def get(self, request):
        # Basic Counts
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_exams = Exam.objects.count()
        total_classes = Class.objects.count()
        total_sessions = Session.objects.count()
        total_subjects = Subject.objects.count()
        total_marks_records = Mark.objects.count()

        # Students per Class
        students_per_class = Class.objects.annotate(
            student_count=Count('students')
        ).values('name', 'student_count')

        # Teachers per Department
        teachers_per_department = Teacher.objects.values('department').annotate(
            count=Count('id')
        ).filter(department__isnull=False)

        # Exams by Type
        exams_by_type = Exam.objects.values('exam_type').annotate(
            count=Count('id')
        )

        # Average Class Size
        avg_class_size = Student.objects.values('class_name').annotate(
            count=Count('id')
        ).aggregate(Avg('count'))['count__avg'] or 0

        # Students per Session
        students_per_session = Session.objects.annotate(
            student_count=Count('students')
        ).values('name', 'student_count')

        # Grade Distribution
        grade_distribution = Mark.objects.values('grade').annotate(
            count=Count('id')
        ).order_by('grade')

        # Overall Statistics
        total_marks_passed = Mark.objects.filter(grade__in=['A+', 'A', 'B+', 'B', 'C+']).count()
        pass_percentage = (total_marks_passed / total_marks_records * 100) if total_marks_records > 0 else 0

        data = {
            # Basic Counts
            'summary': {
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_exams': total_exams,
                'total_classes': total_classes,
                'total_sessions': total_sessions,
                'total_subjects': total_subjects,
                'total_marks_records': total_marks_records,
            },
            
            # Detailed Analytics
            'analytics': {
                'students_per_class': list(students_per_class),
                'teachers_per_department': list(teachers_per_department),
                'exams_by_type': list(exams_by_type),
                'students_per_session': list(students_per_session),
                'grade_distribution': list(grade_distribution),
            },

            # Performance Metrics
            'metrics': {
                'average_class_size': round(avg_class_size, 2),
                'total_marks_passed': total_marks_passed,
                'pass_percentage': round(pass_percentage, 2),
            }
        }
        return Response(data)
