from django.contrib import admin
from .models import ReportDevModel, Build


@admin.register(Build)
class ReportDevAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'device', 'display', 'density', 'sdk', 'version_name', 'version_code']


@admin.register(ReportDevModel)
class ReportDevAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'type', 'build', 'secondParam', 'screenShot', 'logCsvFile']
