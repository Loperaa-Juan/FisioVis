from django.contrib import admin
from .models import Patient
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    model = Patient
    list_display = ["full_name", "phone", 'email']
    search_fields = ['full_name']


admin.site.register(Patient, ProductAdmin)