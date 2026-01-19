from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'class_name', 'session', 'email', 'phone')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('class_name', 'session')
    ordering = ('roll_number',)
    readonly_fields = ('created_at', 'updated_at')
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
