from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'phone', 'post')
    search_fields = ('name', 'subject')
    list_filter = ('subject', 'post')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    