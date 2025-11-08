from django.contrib import admin
from .models import Assessment
# Register your models here.
class AssessmentAdmin(admin.ModelAdmin):
    model = Assessment
    list_display = ["movement_type", 'name']
    search_fields = ['name']
    
admin.site.register(Assessment, AssessmentAdmin)
