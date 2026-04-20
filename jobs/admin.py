from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ['title', 'company', 'location', 'job_type', 'is_active']
    search_fields = ['title', 'company', 'required_skills']
    list_filter   = ['job_type', 'is_active']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['user', 'job', 'status', 'match_score', 'applied_at']
    list_filter   = ['status']