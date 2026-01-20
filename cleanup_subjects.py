#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Subject

print("Fixing Subject Codes and Group Names...")
print("="*60)

# Fix codes with -B, -H suffixes (remove the suffix)
code_fixes = {
    '101-B': '101',
    '102-B': '102',
    '107-B': '107',
    '108-B': '108',
    '275-B': '275',
    '101-H': '101',
    '102-H': '102',
    '107-H': '107',
    '108-H': '108',
    '275-H': '275',
    '109-H': '109',
    '109': '109',  # General Math
}

fixed_count = 0
for old_code, new_code in code_fixes.items():
    subjects = Subject.objects.filter(code=old_code)
    for subject in subjects:
        # Check if subject with new code already exists (different name)
        existing = Subject.objects.filter(code=new_code).exclude(id=subject.id)
        if not existing.exists():
            subject.code = new_code
            subject.save()
            print(f"✓ Fixed: {subject.name} ({old_code} → {new_code})")
            fixed_count += 1
        else:
            # Delete duplicate if it exists with different name
            print(f"⊘ Skipped (duplicate exists): {subject.name} ({old_code})")

# Remove religion group subjects (keep only Science, Business Studies, Humanities)
print("\nRemoving Religion subjects...")
religion_subjects = Subject.objects.filter(group='religion')
deleted_count = 0
for subject in religion_subjects:
    print(f"✗ Deleting: {subject.name} ({subject.code}) - Religion group")
    subject.delete()
    deleted_count += 1

# Create compulsory subjects for all groups (Bangla, English, ICT)
print("\nUpdating compulsory subjects...")
compulsory_data = [
    {'name': 'Bangla', 'code': 'BANGLA', 'category': 'compulsory'},
    {'name': 'English', 'code': 'ENGLISH', 'category': 'compulsory'},
    {'name': 'ICT', 'code': 'ICT', 'category': 'compulsory'},
]

for data in compulsory_data:
    subject, created = Subject.objects.get_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'category': data['category'],
            'group': 'science'  # Default, but it's for all groups
        }
    )
    if created:
        print(f"✓ Created: {subject.name} ({subject.code})")
    else:
        # Update if exists
        if subject.name != data['name']:
            subject.name = data['name']
            subject.category = data['category']
            subject.save()
            print(f"✓ Updated: {subject.name} ({subject.code})")

print(f"\n{'='*60}")
print("Summary:")
print(f"  Fixed codes: {fixed_count}")
print(f"  Deleted religion subjects: {deleted_count}")
print(f"  Total subjects in DB: {Subject.objects.count()}")
print(f"{'='*60}")

# Show groups
print("\nSubjects by Group:")
for group_val, group_name in [('science', 'Science'), ('business', 'Business Studies'), ('humanities', 'Humanities')]:
    count = Subject.objects.filter(group=group_val).count()
    print(f"  {group_name}: {count} subjects")
