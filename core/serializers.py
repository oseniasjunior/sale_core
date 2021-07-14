from rest_framework import serializers
from core import models, serializers_results


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    # cities = CitySerializer(source='city_set', many=True, read_only=True)

    class Meta:
        model = models.State
        fields = '__all__'


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    employees = serializers_results.EmployeesSerializerResult(source='employee_set', many=True, read_only=True)

    class Meta:
        model = models.Department
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zone
        fields = '__all__'
