from django.contrib import admin
from .models import Session, Class, Subject

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Session Information', {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'group', 'category', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('group', 'category')
    ordering = ('group', 'category', 'name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'code')
        }),
        ('Classification', {
            'fields': ('group', 'category', 'class_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
