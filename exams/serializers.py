from rest_framework import serializers
from .models import ExamMark, ExamType
from students.models import Student
from academics.models import Subject, Session


class ExamMarkListSerializer(serializers.ModelSerializer):
    """Serializer for listing exam marks"""
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_group = serializers.CharField(source='student.get_group_display', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    attendance_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamMark
        fields = [
            'id', 'exam_type', 'exam_type_name', 'exam_date', 'student', 'student_name', 
            'student_roll', 'student_group', 'subject', 'subject_name', 'subject_code',
            'cq_marks', 'mct_marks', 'lab_marks', 'total_marks', 'grade',
            'total_class', 'present', 'absent', 'attendance_percentage', 'session'
        ]
    
    def get_attendance_percentage(self, obj):
        """Calculate attendance percentage"""
        if obj.total_class > 0:
            return round((obj.present / obj.total_class) * 100, 2)
        return 0


class ExamMarkDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for exam marks with all information"""
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    student_details = serializers.SerializerMethodField()
    subject_details = serializers.SerializerMethodField()
    attendance_summary = serializers.SerializerMethodField()
    marks_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamMark
        fields = [
            'id', 'exam_type', 'exam_type_name', 'exam_date', 'student', 'student_details',
            'subject', 'subject_details', 'session',
            'cq_marks', 'mct_marks', 'lab_marks', 'total_marks', 'grade',
            'marks_summary', 'total_class', 'present', 'absent', 'attendance_summary',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_marks', 'grade', 'created_at', 'updated_at']
    
    def get_student_details(self, obj):
        """Return detailed student information"""
        return {
            'id': obj.student.id,
            'name': obj.student.name,
            'roll_number': obj.student.roll_number,
            'email': obj.student.email,
            'group': obj.student.get_group_display(),
            'class': obj.student.class_name.name if obj.student.class_name else None,
        }
    
    def get_subject_details(self, obj):
        """Return detailed subject information"""
        return {
            'id': obj.subject.id,
            'name': obj.subject.name,
            'code': obj.subject.code,
            'group': obj.subject.group,
            'category': obj.subject.category,
        }
    
    def get_marks_summary(self, obj):
        """Return summary of marks"""
        return {
            'cq_marks': obj.cq_marks,
            'mct_marks': obj.mct_marks,
            'lab_marks': obj.lab_marks,
            'total_marks': obj.total_marks,
        }
    
    def get_attendance_summary(self, obj):
        """Return attendance summary"""
        attendance_pct = 0
        if obj.total_class > 0:
            attendance_pct = round((obj.present / obj.total_class) * 100, 2)
        
        return {
            'total_class': obj.total_class,
            'present': obj.present,
            'absent': obj.absent,
            'percentage': attendance_pct,
        }


class ExamMarkCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating exam marks"""
    
    class Meta:
        model = ExamMark
        fields = [
            'exam_type', 'exam_date', 'student', 'subject', 'session',
            'cq_marks', 'mct_marks', 'lab_marks',
            'total_class', 'present', 'absent', 'remarks'
        ]
    
    def validate(self, data):
        """Validate marks and attendance data"""
        # Validate attendance
        total_class = data.get('total_class', 10)
        present = data.get('present', 0)
        absent = data.get('absent', 0)
        
        if present + absent > total_class:
            raise serializers.ValidationError(
                "Present + Absent cannot exceed total classes"
            )
        
        # Check for duplicate entry
        exam_type = data.get('exam_type')
        exam_date = data.get('exam_date')
        student = data.get('student')
        subject = data.get('subject')
        session = data.get('session')
        
        # Skip this check on update
        if self.instance is None:
            if ExamMark.objects.filter(
                exam_type=exam_type,
                exam_date=exam_date,
                student=student,
                subject=subject,
                session=session
            ).exists():
                raise serializers.ValidationError(
                    "Marks already exist for this student-subject-exam combination on this date"
                )
        
        return data
