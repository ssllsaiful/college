from django.db import models
from academics.models import Session, Class, Subject

class Student(models.Model):
    GROUP_CHOICES = [
        ('science', 'Science'),
        ('business', 'Business Studies'),
        ('humanities', 'Humanities'),
    ]
    
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='students')
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='student_enrollments', blank=True)
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
    
    def get_subjects_display(self):
        """Return all subject names with || separator"""
        subjects = self.subjects.all()
        if not subjects:
            return '-'
        return ' || '.join([s.name for s in subjects])
    
    def get_subject_codes_display(self):
        """Return all subject codes with || separator"""
        subjects = self.subjects.all()
        if not subjects:
            return '-'
        return ' || '.join([s.code for s in subjects])
