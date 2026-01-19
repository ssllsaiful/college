from django.contrib import admin
from django.utils.html import format_html
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'group', 'get_subjects_display', 'class_name', 'session')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('class_name', 'session', 'group')
    ordering = ('roll_number',)
    readonly_fields = ('created_at', 'updated_at', 'get_all_subjects_display')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'roll_number', 'email', 'phone')
        }),
        ('Academic Info', {
            'fields': ('class_name', 'session', 'group', 'subjects', 'get_all_subjects_display')
        }),
        ('Personal Info', {
            'fields': ('address', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_subjects_display(self, obj):
        """Display all subjects as comma-separated list"""
        subjects = obj.subjects.all()
        if subjects:
            subject_names = [s.name for s in subjects]
            return format_html(
                '<div style="max-width: 300px; word-wrap: break-word;">{}</div>',
                ', '.join(subject_names)
            )
        return '-'
    get_subjects_display.short_description = 'Subjects'
    
    def get_all_subjects_display(self, obj):
        """Display all subjects with details in readonly field"""
        subjects = obj.subjects.all()
        if not subjects:
            return 'No subjects assigned'
        
        html = '<div style="background: #f5f5f5; padding: 10px; border-radius: 4px;">'
        html += '<table style="width: 100%; border-collapse: collapse;">'
        html += '<tr style="background: #e0e0e0;"><th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Subject</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Code</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Group</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Category</th></tr>'
        
        for subject in subjects:
            html += f'<tr style="border: 1px solid #ddd;"><td style="padding: 8px; border: 1px solid #ccc;">{subject.name}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{subject.code}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{subject.group or "-"}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{subject.get_category_display()}</td></tr>'
        
        html += '</table></div>'
        return format_html(html)
    get_all_subjects_display.short_description = 'All Subjects'

