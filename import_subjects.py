#!/usr/bin/env python
import os
import sys
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Subject

def import_subjects_from_json(filepath):
    """Import subjects from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    subjects = data.get('subjects', [])
    created_count = 0
    skipped_count = 0
    errors = []
    
    for subject_data in subjects:
        try:
            name = subject_data.get('name')
            code = subject_data.get('code')
            group = subject_data.get('group', 'science')
            category = subject_data.get('category', 'optional')
            
            # Check if subject already exists
            if Subject.objects.filter(code=code).exists():
                skipped_count += 1
                print(f"⊘ Skipped: {name} ({code}) - Already exists")
                continue
            
            # Create subject
            Subject.objects.create(
                name=name,
                code=code,
                group=group,
                category=category
            )
            created_count += 1
            print(f"✓ Created: {name} ({code}) - Group: {group}, Category: {category}")
        except Exception as e:
            skipped_count += 1
            error_msg = f"✗ Error: {subject_data.get('name')} ({subject_data.get('code')}) - {str(e)}"
            print(error_msg)
            errors.append(error_msg)
    
    print(f"\n{'='*60}")
    print(f"Import Summary:")
    print(f"  Created:  {created_count}")
    print(f"  Skipped:  {skipped_count}")
    print(f"  Errors:   {len(errors)}")
    print(f"  Total:    {len(subjects)}")
    print(f"{'='*60}")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  {error}")

if __name__ == "__main__":
    filepath = '/home/saifulislam/saiful/college/subjects_data.json'
    import_subjects_from_json(filepath)
