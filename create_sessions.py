#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_project.settings')
sys.path.insert(0, '/home/saifulislam/saiful/college')
django.setup()

from academics.models import Session

# Sample sessions
sessions_data = [
    '2024-2025',
    '2025-2026',
    '2026-2027',
]

for session_name in sessions_data:
    session, created = Session.objects.get_or_create(name=session_name)
    if created:
        print(f"✓ Created session: {session_name}")
    else:
        print(f"⊘ Session already exists: {session_name}")

print(f"\nTotal Sessions: {Session.objects.count()}")
for session in Session.objects.all().order_by('-name'):
    print(f"  - {session.name}")
