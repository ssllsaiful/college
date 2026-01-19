from rest_framework import serializers
from .models import Student
from academics.serializers import SubjectSerializer

class StudentListSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_name.name', read_only=True)
    session = serializers.CharField(source='session.name', read_only=True)
    group = serializers.CharField(source='get_group_display', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_display = serializers.SerializerMethodField()
    subject_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'class_name', 'session', 'group', 'email', 'phone', 'subjects', 'subjects_display', 'subject_count']
    
    def get_subjects_display(self, obj):
        """Return subjects with || separator"""
        subjects = obj.subjects.all()
        if not subjects:
            return '-'
        return ' || '.join([s.name for s in subjects])
    
    def get_subject_count(self, obj):
        return obj.subjects.count()

class StudentDetailSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_name.name', read_only=True)
    session = serializers.CharField(source='session.name', read_only=True)
    group = serializers.CharField(source='get_group_display', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'class_name', 'session', 'group', 'email', 'phone', 'address', 'date_of_birth', 'subjects', 'subjects_display', 'created_at']
    
    def get_subjects_display(self, obj):
        """Return subjects with || separator"""
        subjects = obj.subjects.all()
        if not subjects:
            return '-'
        return ' || '.join([s.name for s in subjects])

