from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['id_number', 'first_name', 'last_name']
