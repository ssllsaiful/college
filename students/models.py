from django.db import models
from academics.models import Session, Class, Subject

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='students')
    subjects = models.ManyToManyField(Subject, through='StudentSubject', related_name='students')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roll_number']
    
    def __str__(self):
        return f"{self.name} - {self.roll_number}"


class StudentSubject(models.Model):
    """Relationship between Student and Subject"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_enrollments')
    group = models.CharField(max_length=20, choices=[
        ('science', 'Science'),
        ('business', 'Business'),
        ('humanities', 'Humanities'),
        ('religion', 'Religion'),
    ], blank=True, null=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject')
        ordering = ['subject__name']
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"