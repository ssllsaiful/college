from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user', 'subject', 'phone', 'post')
    search_fields = ('name', 'subject', 'user__username')
    list_filter = ('subject', 'post')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Basic Info', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Academic Info', {
            'fields': ('subject', 'post', 'qualification', 'department')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_user(self, obj):
        """Display linked user account"""
        if obj.user:
            return f"{obj.user.username} ({obj.user.get_role_display()})"
        return "-"
    get_user.short_description = 'User Account'
    