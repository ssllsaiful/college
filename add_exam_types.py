#!/usr/bin/env python
"""
Script to add default exam types to the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
django.setup()

from exams.models import ExamType

# Default exam types
exam_types = [
    {
        'name': 'CT-Exam',
        'description': 'Class Test Examination'
    },
    {
        'name': 'Mid-Term',
        'description': 'Mid-Term Examination'
    },
    {
        'name': 'Half Yearly',
        'description': 'Half Yearly Examination'
    },
    {
        'name': 'Test',
        'description': 'General Test'
    },
    {
        'name': 'Pre-test',
        'description': 'Pre-test or Pre-exam'
    },
    {
        'name': 'Year Final',
        'description': 'Final Year Examination'
    },
]

print("Adding default exam types...")
print("=" * 60)

created_count = 0
for exam_type_data in exam_types:
    exam_type, created = ExamType.objects.get_or_create(
        name=exam_type_data['name'],
        defaults={
            'description': exam_type_data['description'],
            'is_active': True
        }
    )
    if created:
        print(f"✓ Created: {exam_type.name}")
        created_count += 1
    else:
        print(f"⊘ Already exists: {exam_type.name}")

print("=" * 60)
print(f"Summary: {created_count} new exam types created")
print(f"Total exam types: {ExamType.objects.count()}")
print("\nNow you can:")
print("1. Go to /admin/exams/examtype/ to manage exam types")
print("2. Add, edit, or delete exam types as needed")
print("3. Each exam type will appear in the Exam form dropdown")
