from django.db import models


class ReportDevModel(models.Model):
    email = models.CharField(max_length=100)
    secondParam = models.CharField(max_length=10000)
    screenShot = models.CharField(max_length=10000)
    logCsvFile = models.CharField(max_length=10000)

    class Meta:
        db_table = "Report"