from rest_framework import serializers
from core import models


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zone
        fields = '__all__'
