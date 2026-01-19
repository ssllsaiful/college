from django.contrib import admin
from .models import Student, StudentSubject

class StudentSubjectInline(admin.TabularInline):
    model = StudentSubject
    extra = 1
    fields = ('subject', 'group')
    autocomplete_fields = ('subject',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'class_name', 'session', 'email', 'phone')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('class_name', 'session')
    ordering = ('roll_number',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StudentSubjectInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'roll_number', 'email', 'phone')
        }),
        ('Academic Info', {
            'fields': ('class_name', 'session')
        }),
        ('Personal Info', {
            'fields': ('address', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

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

