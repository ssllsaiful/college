from django.contrib import admin
from .models import Exam, Mark

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

@admin.register(Mark)
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
