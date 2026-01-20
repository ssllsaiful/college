from django.shortcuts import render
from django.db.models import Count, Avg, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from students.models import Student
from teachers.models import Teacher
from exams.models import ExamMark, ExamType
from academics.models import Class, Session, Subject

class DashboardView(APIView):
    def get(self, request):
        # Basic Counts
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_exam_marks = ExamMark.objects.count()
        total_exam_types = ExamType.objects.count()
        total_classes = Class.objects.count()
        total_sessions = Session.objects.count()
        total_subjects = Subject.objects.count()

        # Students per Class
        students_per_class = Class.objects.annotate(
            student_count=Count('students')
        ).values('name', 'student_count')

        # Teachers per Department
        teachers_per_department = Teacher.objects.values('department').annotate(
            count=Count('id')
        ).filter(department__isnull=False)

        # Exam Marks by Type
        marks_by_exam_type = ExamMark.objects.values('exam_type__name').annotate(
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

        # Grade Distribution from ExamMarks
        grade_distribution = ExamMark.objects.values('grade').annotate(
            count=Count('id')
        ).order_by('grade').filter(grade__isnull=False)

        # Overall Statistics
        total_marks_with_grade = ExamMark.objects.filter(grade__isnull=False).count()
        excellent_grades = ExamMark.objects.filter(grade__in=['A+', 'A']).count()
        good_grades = ExamMark.objects.filter(grade__in=['A-', 'B']).count()
        pass_percentage = (excellent_grades / total_marks_with_grade * 100) if total_marks_with_grade > 0 else 0
        
        # Average marks and attendance
        avg_marks = ExamMark.objects.filter(total_marks__isnull=False).aggregate(
            avg=Avg('total_marks')
        )['avg'] or 0
        avg_attendance = ExamMark.objects.filter(total_class__gt=0).aggregate(
            avg=Avg((Count('present') * 100 / Count('total_class')))
        )['avg'] or 0

        data = {
            # Basic Counts
            'summary': {
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_exam_marks': total_exam_marks,
                'total_exam_types': total_exam_types,
                'total_classes': total_classes,
                'total_sessions': total_sessions,
                'total_subjects': total_subjects,
            },
            
            # Detailed Analytics
            'analytics': {
                'students_per_class': list(students_per_class),
                'teachers_per_department': list(teachers_per_department),
                'marks_by_exam_type': list(marks_by_exam_type),
                'students_per_session': list(students_per_session),
                'grade_distribution': list(grade_distribution),
            },

            # Performance Metrics
            'metrics': {
                'average_class_size': round(avg_class_size, 2),
                'excellent_grades_count': excellent_grades,
                'good_grades_count': good_grades,
                'excellent_pass_percentage': round(pass_percentage, 2),
                'average_marks': round(avg_marks, 2),
            }
        }
        return Response(data)
