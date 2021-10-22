# Generated by Django 3.2.8 on 2021-10-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDevModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('type', models.CharField(max_length=11)),
                ('secondParam', models.TextField(max_length=10000)),
                ('screenShot', models.CharField(max_length=10000)),
                ('logCsvFile', models.CharField(max_length=10000)),
            ],
            options={
                'db_table': 'Report',
            },
        ),
    ]
