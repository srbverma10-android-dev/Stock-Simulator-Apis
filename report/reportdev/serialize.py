from rest_framework import serializers
from .models import ReportDevModel


class ReportSerialize(serializers.ModelSerializer):
    class Meta:
        model = ReportDevModel
        fields = "__all__"
