#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Class, Session, Subject
from students.models import Student

# Create a sample class if it doesn't exist
class_obj, _ = Class.objects.get_or_create(
    code='XA',
    defaults={'name': 'XI-A Science'}
)

# Get a session
session = Session.objects.filter(name='2025-2026').first()
if not session:
    session = Session.objects.first()

print(f"\nCreating sample students with subjects...")
print(f"Class: {class_obj.name} ({class_obj.code})")
print(f"Session: {session.name}\n")

# Sample students
students_data = [
    {
        'name': 'Fatima Khan',
        'roll_number': '20356',
        'email': 'fatima@example.com',
        'group': 'science',
        'subjects': ['101', '107', '176', '177', '275'],  # Bangla, English, Chemistry 1&2, ICT
    },
    {
        'name': 'Ahmed Hassan',
        'roll_number': '20365',
        'email': 'ahmed@example.com',
        'group': 'science',
        'subjects': ['101', '107', '174', '175', '265'],  # Bangla, English, Physics 1&2, Higher Math 1
    },
]

for student_data in students_data:
    student, created = Student.objects.get_or_create(
        roll_number=student_data['roll_number'],
        defaults={
            'name': student_data['name'],
            'email': student_data['email'],
            'class_name': class_obj,
            'session': session,
            'group': student_data['group'],
        }
    )
    
    if created:
        print(f"✓ Created student: {student.name} ({student.roll_number})")
    else:
        print(f"⊘ Student already exists: {student.name}")
    
    # Add subjects
    for subject_code in student_data['subjects']:
        try:
            subject = Subject.objects.get(code=subject_code)
            student.subjects.add(subject)
            print(f"  → Added subject: {subject.name} ({subject.code})")
        except Subject.DoesNotExist:
            print(f"  ✗ Subject not found: {subject_code}")

print(f"\n{'='*60}")
print("Summary - Student List View:")
print(f"{'='*60}")
for student in Student.objects.all():
    subjects = student.subjects.all()
    print(f"\nName: {student.name}")
    print(f"Roll Number: {student.roll_number}")
    print(f"Group: {student.get_group_display() or '-'}")
    print(f"Class: {student.class_name.name}")
    print(f"Subjects: {student.get_subjects_display()}")

