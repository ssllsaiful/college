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