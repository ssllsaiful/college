from django.db import models

# Create your models here.
from django.db import models

class Session(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Format: YYYY-YYYY (e.g., 2024-2025)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-name']
    
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    GROUP_CHOICES = [
        ('science', 'Science Group (বিজ্ঞান বিভাগ)'),
        ('business', 'Business Studies Group (ব্যবসায় শিক্ষা বিভাগ)'),
        ('humanities', 'Humanities Group (মানবিক বিভাগ)'),
        ('religion', 'Religion (ধর্ম)'),
    ]
    
    CATEGORY_CHOICES = [
        ('compulsory', 'Compulsory Subjects'),
        ('group', 'Group Subjects'),
        ('optional', 'Optional / 4th Subjects'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='science')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='compulsory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['group', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def __str__(self):
        return f"{self.name} ({self.class_name})"