from django.contrib import admin
from django.utils.html import format_html
from .models import ExamType, ExamMark

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    """Manage exam types - add/remove as needed"""
    list_display = ('name', 'description_short', 'is_active', 'get_active_status')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Exam Type Info', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def description_short(self, obj):
        """Show truncated description"""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_short.short_description = 'Description'
    
    def get_active_status(self, obj):
        """Display active status with color"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Inactive</span>'
        )
    get_active_status.short_description = 'Status'


@admin.register(ExamMark)
class ExamMarkAdmin(admin.ModelAdmin):
    """
    Unified admin interface for all exam marks:
    - Flexible exam types (from ExamType)
    - Multiple mark components (CQ, MCT, LAB)
    - Attendance tracking
    - Auto-calculated grades
    """
    list_display = ('get_exam_type', 'exam_date', 'student', 'subject', 'get_marks_display', 'grade', 'attendance_display')
    search_fields = ('student__name', 'student__roll_number', 'subject__name', 'exam_type__name')
    list_filter = ('exam_type', 'subject', 'session', 'student__group', 'grade')
    ordering = ('-exam_date', 'student__roll_number')
    readonly_fields = ('total_marks', 'grade', 'created_at', 'updated_at')
    date_hierarchy = 'exam_date'
    
    fieldsets = (
        ('Exam Information', {
            'fields': ('exam_type', 'exam_date', 'student', 'subject', 'session')
        }),
        ('Mark Components', {
            'fields': ('cq_marks', 'mct_marks', 'lab_marks', 'total_marks', 'grade'),
            'description': 'CQ = Constructed Question, MCT = Multiple Choice Test, LAB = Laboratory. Total and Grade are auto-calculated.'
        }),
        ('Attendance Tracking', {
            'fields': ('total_class', 'present', 'absent'),
            'description': 'Total Classes: Total classes in the course, Present: Classes attended, Absent: Classes missed'
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_exam_type(self, obj):
        """Display exam type with color coding"""
        colors = {
            'ct_exam': '#0066cc',
            'midterm': '#ff6600',
            'half_yearly': '#009900',
            'test': '#cc0000',
            'pretest': '#9900cc',
            'year_final': '#ff0000',
        }
        # Get color from exam type or use default
        color = colors.get(obj.exam_type.name.lower().replace(' ', '_').replace('-', '_'), '#666666')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.exam_type.name
        )
    get_exam_type.short_description = 'Exam Type'
    
    def get_marks_display(self, obj):
        """Display mark components compactly"""
        parts = []
        if obj.cq_marks is not None:
            parts.append(f"CQ:{obj.cq_marks}")
        if obj.mct_marks is not None:
            parts.append(f"MCT:{obj.mct_marks}")
        if obj.lab_marks is not None:
            parts.append(f"LAB:{obj.lab_marks}")
        return " | ".join(parts) if parts else "-"
    get_marks_display.short_description = 'Marks (CQ|MCT|LAB)'
    
    def attendance_display(self, obj):
        """Display attendance summary with percentage"""
        if obj.total_class > 0:
            attendance_pct = (obj.present / obj.total_class) * 100
            return format_html(
                '<span>{}/{} ({:.0f}%)</span>',
                obj.present,
                obj.total_class,
                attendance_pct
            )
        return "-"
    attendance_display.short_description = 'Attendance'
    
    def get_readonly_fields(self, request, obj=None):
        """Make calculated fields always read-only"""
        return self.readonly_fields
