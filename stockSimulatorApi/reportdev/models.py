from django.db import models


class Build(models.Model):
    brand = models.CharField(max_length=100, null=True)
    device = models.CharField(max_length=100, null=True)
    display = models.CharField(max_length=100, null=True)
    density = models.CharField(max_length=100, null=True)
    sdk = models.CharField(max_length=100, null=True)
    version_name = models.CharField(max_length=100, null=True)
    version_code = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "Build"


class ReportDevModel(models.Model):
    email = models.EmailField(max_length=100)
    type = models.CharField(max_length=11)
    secondParam = models.TextField(max_length=10000)
    build = models.ForeignKey(to=Build, on_delete=models.SET_NULL, null=True)
    screenShot = models.CharField(max_length=10000)
    logCsvFile = models.CharField(max_length=10000)

    class Meta:
        db_table = "Report"
