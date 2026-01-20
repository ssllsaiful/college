from django.db import models

# Create your models here.
from django.db import models
from academics.models import Subject, Class, Session
from students.models import Student

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Mid Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"
    
    class Meta:
        ordering = ['-exam_date']

class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.exam.name}: {self.marks_obtained}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade based on percentage
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
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
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['student__roll_number']


class ExamMark(models.Model):
    """Model to track CT marks with multiple components and attendance"""
    EXAM_NAME_CHOICES = [
        ('ct_exam', 'CT-Exam'),
        ('midterm', 'Mid-Term'),
        ('half_yearly', 'Half Yearly'),
        ('test', 'Test'),
        ('pretest', 'Pre-test'),
        ('year_final', 'Year Final'),
    ]
    
    # Basic information
    exam_name = models.CharField(max_length=20, choices=EXAM_NAME_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_marks')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exam_marks')
    
    # Mark components (CQ = Constructed Question, MCT = Multiple Choice Test, LAB = Laboratory)
    cq_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Constructed Question marks")
    mct_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Multiple Choice Test marks")
    lab_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Laboratory marks")
    
    # Attendance tracking
    total_class = models.IntegerField(default=10, help_text="Total classes in the course")
    present = models.IntegerField(default=0, help_text="Classes attended")
    absent = models.IntegerField(default=0, help_text="Classes missed")
    
    # Total marks (calculated)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Total marks obtained")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.get_exam_name_display()} - {self.subject.name}"
    
    def save(self, *args, **kwargs):
        """Calculate total marks from components"""
        marks_list = [m for m in [self.cq_marks, self.mct_marks, self.lab_marks] if m is not None]
        if marks_list:
            self.total_marks = sum(marks_list)
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('exam_name', 'student', 'subject', 'session')
        ordering = ['student__roll_number', 'subject__name']
        verbose_name = 'Exam Mark'
        verbose_name_plural = 'Exam Marks'