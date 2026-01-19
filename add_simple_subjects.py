#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Subject

# Simple subjects to add (without 1st/2nd Paper)
simple_subjects = [
    # Compulsory subjects
    {'name': 'Bangla', 'code': 'BANGLA', 'group': 'science', 'category': 'compulsory'},
    {'name': 'English', 'code': 'ENGLISH', 'group': 'science', 'category': 'compulsory'},
    {'name': 'ICT (Basic)', 'code': 'ICT-BASIC', 'group': 'science', 'category': 'compulsory'},
    
    # Science subjects
    {'name': 'Physics', 'code': 'PHYSICS', 'group': 'science', 'category': 'group'},
    {'name': 'Chemistry', 'code': 'CHEMISTRY', 'group': 'science', 'category': 'group'},
    {'name': 'Biology', 'code': 'BIOLOGY', 'group': 'science', 'category': 'group'},
    {'name': 'Mathematics', 'code': 'MATHEMATICS', 'group': 'science', 'category': 'group'},
    
    # Business subjects
    {'name': 'Accounting', 'code': 'ACCOUNTING', 'group': 'business', 'category': 'group'},
    {'name': 'Management', 'code': 'MANAGEMENT', 'group': 'business', 'category': 'group'},
    {'name': 'Economics', 'code': 'ECONOMICS', 'group': 'business', 'category': 'group'},
    
    # Humanities subjects
    {'name': 'History', 'code': 'HISTORY', 'group': 'humanities', 'category': 'group'},
    {'name': 'Geography', 'code': 'GEOGRAPHY', 'group': 'humanities', 'category': 'group'},
    {'name': 'Civics', 'code': 'CIVICS', 'group': 'humanities', 'category': 'group'},
    
    # Religion
    {'name': 'Islamic Studies', 'code': 'ISLAMIC-STUDIES', 'group': 'religion', 'category': 'compulsory'},
    {'name': 'Hindu Religion', 'code': 'HINDU-RELIGION', 'group': 'religion', 'category': 'compulsory'},
]

created_count = 0
skipped_count = 0

for subject_data in simple_subjects:
    subject, created = Subject.objects.get_or_create(
        code=subject_data['code'],
        defaults={
            'name': subject_data['name'],
            'group': subject_data['group'],
            'category': subject_data['category'],
        }
    )
    
    if created:
        created_count += 1
        print(f"✓ Created: {subject.name} ({subject.code})")
    else:
        skipped_count += 1
        print(f"⊘ Already exists: {subject.name} ({subject.code})")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Created: {created_count}")
print(f"  Skipped: {skipped_count}")
print(f"  Total Subjects in DB: {Subject.objects.count()}")
print(f"{'='*60}")
