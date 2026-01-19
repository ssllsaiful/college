from rest_framework import serializers
from .models import Student, StudentSubject
from academics.serializers import SubjectSerializer

class StudentSubjectSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    
    class Meta:
        model = StudentSubject
        fields = ['id', 'subject', 'subject_details', 'group', 'enrollment_date']

class StudentDetailSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_name.name', read_only=True)
    session = serializers.CharField(source='session.name', read_only=True)
    student_subjects = StudentSubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'class_name', 'session', 'email', 'phone', 'address', 'date_of_birth', 'student_subjects', 'created_at']

class StudentListSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_name.name', read_only=True)
    session = serializers.CharField(source='session.name', read_only=True)
    subject_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'class_name', 'session', 'email', 'phone', 'subject_count']
    
    def get_subject_count(self, obj):
        return obj.subjects.count()
