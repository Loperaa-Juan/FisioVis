from django.contrib import admin

from .models import Assessment, PatientAssessment


# Register your models here.
class AssessmentAdmin(admin.ModelAdmin):
    model = Assessment
    list_display = ["movement_type", "name"]
    search_fields = ["name"]


admin.site.register(Assessment, AssessmentAdmin)


class PatientAssessmentAdmin(admin.ModelAdmin):
    model = PatientAssessment
    list_display = ["patient", "date", "angle", "assessment"]
    search_fields = ["date"]


admin.site.register(PatientAssessment, PatientAssessmentAdmin)
