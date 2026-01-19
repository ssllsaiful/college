from django.contrib import admin
from .models import Session, Class, Subject

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year', 'created_at')
    search_fields = ('name',)
    ordering = ('-start_year',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'class_name', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('class_name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
