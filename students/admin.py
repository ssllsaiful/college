from django.contrib import admin
from django.utils.html import format_html
from .models import Student, StudentSubject

class StudentSubjectInline(admin.TabularInline):
    model = StudentSubject
    extra = 1
    fields = ('subject', 'group')
    autocomplete_fields = ('subject',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'get_group', 'get_subjects', 'class_name', 'session')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('class_name', 'session', 'student_subjects__group')
    ordering = ('roll_number',)
    readonly_fields = ('created_at', 'updated_at', 'get_all_subjects_display')
    inlines = [StudentSubjectInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'roll_number', 'email', 'phone')
        }),
        ('Academic Info', {
            'fields': ('class_name', 'session', 'get_all_subjects_display')
        }),
        ('Personal Info', {
            'fields': ('address', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_group(self, obj):
        """Display primary group for student"""
        groups = obj.student_subjects.values_list('group', flat=True).distinct()
        if groups:
            return ', '.join(g.title() for g in groups if g)
        return '-'
    get_group.short_description = 'Group'
    
    def get_subjects(self, obj):
        """Display all subjects as comma-separated list"""
        subjects = obj.student_subjects.all()
        if subjects:
            subject_names = [ss.subject.name for ss in subjects]
            return format_html(
                '<div style="max-width: 300px; word-wrap: break-word;">{}</div>',
                ', '.join(subject_names)
            )
        return '-'
    get_subjects.short_description = 'Subjects'
    
    def get_all_subjects_display(self, obj):
        """Display all subjects with details in readonly field"""
        subjects = obj.student_subjects.all()
        if not subjects:
            return 'No subjects assigned'
        
        html = '<div style="background: #f5f5f5; padding: 10px; border-radius: 4px;">'
        html += '<table style="width: 100%; border-collapse: collapse;">'
        html += '<tr style="background: #e0e0e0;"><th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Subject</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Code</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Group</th>'
        html += '<th style="padding: 8px; text-align: left; border: 1px solid #ccc;">Category</th></tr>'
        
        for ss in subjects:
            html += f'<tr style="border: 1px solid #ddd;"><td style="padding: 8px; border: 1px solid #ccc;">{ss.subject.name}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{ss.subject.code}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{ss.group or "-"}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ccc;">{ss.subject.get_category_display()}</td></tr>'
        
        html += '</table></div>'
        return format_html(html)
    get_all_subjects_display.short_description = 'All Subjects'

@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'group', 'enrollment_date')
    search_fields = ('student__name', 'subject__name')
    list_filter = ('group', 'enrollment_date')
    readonly_fields = ('enrollment_date',)
    fieldsets = (
        ('Enrollment', {
            'fields': ('student', 'subject', 'group')
        }),
        ('Timestamps', {
            'fields': ('enrollment_date',)
        }),
    )

