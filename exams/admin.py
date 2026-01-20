from django.contrib import admin
from django.utils.html import format_html
from .models import Exam, Mark, ExamMark

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'subject', 'class_name', 'exam_date', 'total_marks')
    search_fields = ('name', 'subject__name')
    list_filter = ('exam_type', 'subject', 'class_name', 'session')
    ordering = ('-exam_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Exam Info', {
            'fields': ('name', 'exam_type', 'exam_date')
        }),
        ('Academic Info', {
            'fields': ('subject', 'class_name', 'session', 'total_marks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ExamMark)
class ExamMarkAdmin(admin.ModelAdmin):
    """Admin interface for CT marks entry with tabular layout"""
    list_display = ('get_exam_display', 'student', 'subject', 'cq_marks', 'mct_marks', 'lab_marks', 'total_marks', 'attendance_display')
    search_fields = ('student__name', 'student__roll_number', 'subject__name', 'exam_name')
    list_filter = ('exam_name', 'subject', 'session', 'student__group')
    ordering = ('exam_name', 'student__roll_number')
    readonly_fields = ('total_marks', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Exam & Student Info', {
            'fields': ('exam_name', 'student', 'subject', 'session')
        }),
        ('Mark Components', {
            'fields': ('cq_marks', 'mct_marks', 'lab_marks', 'total_marks'),
            'description': 'CQ = Constructed Question, MCT = Multiple Choice Test, LAB = Laboratory'
        }),
        ('Attendance Tracking', {
            'fields': ('total_class', 'present', 'absent'),
            'description': 'Total Classes: Total classes in the course, Present: Classes attended, Absent: Classes missed'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_exam_display(self, obj):
        """Display exam name with color coding"""
        colors = {
            'ct_exam': '#0066cc',
            'midterm': '#ff6600',
            'half_yearly': '#009900',
            'test': '#cc0000',
            'pretest': '#9900cc',
            'year_final': '#ff0000',
        }
        color = colors.get(obj.exam_name, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_exam_name_display()
        )
    get_exam_display.short_description = 'Exam Name'
    
    def attendance_display(self, obj):
        """Display attendance summary"""
        if obj.total_class > 0:
            attendance_pct = (obj.present / obj.total_class) * 100
            return f"{obj.present}/{obj.total_class} ({attendance_pct:.0f}%)"
        return "-"
    attendance_display.short_description = 'Attendance'
    
    def get_readonly_fields(self, request, obj=None):
        """Make total_marks always read-only since it's auto-calculated"""
        if obj:
            return self.readonly_fields
        return self.readonly_fields@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'grade')
    search_fields = ('student__name', 'exam__name')
    list_filter = ('grade', 'exam', 'created_at')
    ordering = ('-exam__exam_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Mark Info', {
            'fields': ('student', 'exam', 'marks_obtained', 'grade')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
