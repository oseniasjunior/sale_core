from rest_framework import serializers


class TotalEmployeeByDepartmentSerializerResult(serializers.Serializer):
    department = serializers.CharField(read_only=True, source='name')
    counter = serializers.IntegerField(read_only=True)


class EmployeesSerializerResult(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
