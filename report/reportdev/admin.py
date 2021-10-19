from django.contrib import admin
from .models import ReportDevModel


@admin.register(ReportDevModel)
class ReportDevAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'secondParam']
