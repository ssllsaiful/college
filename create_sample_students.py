#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Class, Session, Subject
from students.models import Student, StudentSubject

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
        'name': 'Ahmed Hassan',
        'roll_number': 'XI-A-001',
        'email': 'ahmed@example.com',
        'subjects': ['101', '107', '174', '175', '275'],  # Bangla, English, Physics 1&2, ICT
        'group': 'science'
    },
    {
        'name': 'Fatima Khan',
        'roll_number': 'XI-A-002',
        'email': 'fatima@example.com',
        'subjects': ['101', '107', '176', '177', '275'],  # Bangla, English, Chemistry 1&2, ICT
        'group': 'science'
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
            student_subject, created = StudentSubject.objects.get_or_create(
                student=student,
                subject=subject,
                defaults={'group': student_data['group']}
            )
            if created:
                print(f"  → Added subject: {subject.name} ({subject.code})")
        except Subject.DoesNotExist:
            print(f"  ✗ Subject not found: {subject_code}")

print(f"\n{'='*60}")
print("Summary:")
print(f"{'='*60}")
for student in Student.objects.all():
    subjects = student.student_subjects.all()
    print(f"\n{student.name} ({student.roll_number})")
    print(f"  Class: {student.class_name.name}")
    print(f"  Session: {student.session.name}")
    print(f"  Subjects ({subjects.count()}):")
    for ss in subjects:
        print(f"    - {ss.subject.name} ({ss.subject.code}) [{ss.group}]")
