from django.db import models
from academics.models import Subject, Session
from students.models import Student


class ExamType(models.Model):
    """Flexible exam type model - add/remove exam names as needed"""
    name = models.CharField(max_length=100, unique=True, help_text="Exam name (e.g., CT-Exam, Mid-Term, Half Yearly, Test, Pre-test, Year Final)")
    description = models.TextField(blank=True, null=True, help_text="Description of this exam type")
    is_active = models.BooleanField(default=True, help_text="Enable/disable this exam type")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Exam Type'
        verbose_name_plural = 'Exam Types'
    
    def __str__(self):
        return self.name


class ExamMark(models.Model):
    """
    Unified model to track all student marks with:
    - Multiple mark components (CQ, MCT, LAB)
    - Flexible exam types via ExamType
    - Attendance tracking
    - Auto-calculated grades
    
    Replaces redundant Exam and Mark models.
    """
    
    # Core information
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exam_marks', help_text="Exam type (CT-Exam, Mid-Term, etc.)")
    exam_date = models.DateField(help_text="Date of the exam")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_marks')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exam_marks')
    
    # Mark components (CQ = Constructed Question, MCT = Multiple Choice Test, LAB = Laboratory)
    cq_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Constructed Question marks")
    mct_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Multiple Choice Test marks")
    lab_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Laboratory marks")
    
    # Total marks and grade
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Total marks obtained (auto-calculated)")
    grade = models.CharField(max_length=5, blank=True, null=True, help_text="Letter grade (auto-calculated)")
    
    # Attendance tracking
    total_class = models.IntegerField(default=10, help_text="Total classes in the course")
    present = models.IntegerField(default=0, help_text="Classes attended")
    absent = models.IntegerField(default=0, help_text="Classes missed")
    
    # Additional info
    remarks = models.TextField(blank=True, null=True, help_text="Teacher remarks or comments")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.exam_type.name} - {self.subject.name}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total_marks and grade"""
        # Calculate total marks from components
        marks_list = [m for m in [self.cq_marks, self.mct_marks, self.lab_marks] if m is not None]
        if marks_list:
            self.total_marks = sum(marks_list)
        else:
            self.total_marks = None
        
        # Auto-calculate grade based on percentage (assuming 100 total from components)
        if self.total_marks:
            percentage = self.total_marks  # Since components add up to total
            if percentage >= 80:
                self.grade = 'A+'
            elif percentage >= 70:
                self.grade = 'A'
            elif percentage >= 60:
                self.grade = 'A-'
            elif percentage >= 50:
                self.grade = 'B'
            elif percentage >= 40:
                self.grade = 'C'
            else:
                self.grade = 'F'
        else:
            self.grade = None
        
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('exam_type', 'exam_date', 'student', 'subject', 'session')
        ordering = ['-exam_date', 'student__roll_number', 'subject__name']
        verbose_name = 'Exam Mark'
        verbose_name_plural = 'Exam Marks'
        indexes = [
            models.Index(fields=['student', 'session']),
            models.Index(fields=['exam_type', 'subject', 'session']),
        ]