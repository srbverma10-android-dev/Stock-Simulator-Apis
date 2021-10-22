from django.contrib import admin
from .models import ReportDevModel, Build


@admin.register(Build)
class ReportDevAdmin(admin.ModelAdmin):
    list_display = ['id', 'buildName']


@admin.register(ReportDevModel)
class ReportDevAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'type', 'build', 'secondParam', 'screenShot', 'logCsvFile']
