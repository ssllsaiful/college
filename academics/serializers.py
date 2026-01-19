from rest_framework import serializers
from .models import Subject, Class, Session

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'class_name', 'group', 'category', 'created_at']

class BulkSubjectImportSerializer(serializers.Serializer):
    subjects = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            help_text="Dict with keys: name, code, group, category"
        ),
        help_text="List of subjects to import"
    )

    def create(self, validated_data):
        subjects_data = validated_data['subjects']
        created_subjects = []
        errors = []

        for idx, subject_data in enumerate(subjects_data):
            try:
                # Validate required fields
                if not subject_data.get('name') or not subject_data.get('code'):
                    errors.append({
                        'index': idx,
                        'error': 'name and code are required',
                        'data': subject_data
                    })
                    continue

                # Check if subject already exists
                if Subject.objects.filter(code=subject_data['code']).exists():
                    errors.append({
                        'index': idx,
                        'error': f"Subject with code {subject_data['code']} already exists",
                        'data': subject_data
                    })
                    continue

                # Create subject
                subject = Subject.objects.create(
                    name=subject_data['name'],
                    code=subject_data['code'],
                    group=subject_data.get('group', 'science'),
                    category=subject_data.get('category', 'compulsory'),
                    class_name=None  # Can be assigned later
                )
                created_subjects.append(subject)

            except Exception as e:
                errors.append({
                    'index': idx,
                    'error': str(e),
                    'data': subject_data
                })

        return {
            'created_subjects': created_subjects,
            'errors': errors,
            'total_created': len(created_subjects),
            'total_errors': len(errors)
        }
