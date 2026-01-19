#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Subject
from django.db.models import Count

# Overall count
total = Subject.objects.count()
print(f"Total Subjects: {total}\n")

# By Group
print("By Group:")
groups = Subject.objects.values('group').annotate(count=Count('id')).order_by('group')
for item in groups:
    print(f"  {item['group']}: {item['count']}")

# By Category
print("\nBy Category:")
categories = Subject.objects.values('category').annotate(count=Count('id')).order_by('category')
for item in categories:
    print(f"  {item['category']}: {item['count']}")

# Sample subjects by group
print("\nSample Subjects:")
for group in ['science', 'business', 'humanities', 'religion']:
    subjects = Subject.objects.filter(group=group)[:3]
    print(f"\n{group.title()}:")
    for s in subjects:
        print(f"  - {s.name} ({s.code}) [{s.category}]")
