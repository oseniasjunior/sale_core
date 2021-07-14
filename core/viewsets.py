from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models, serializers, queries, serializers_results, filters


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer
    filter_class = filters.StateFilter


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    @action(detail=False, methods=['GET'])
    def total_employee(self, request, *args, **kwargs):
        queryset = queries.employee_by_department()
        result = serializers_results.TotalEmployeeByDepartmentSerializerResult(
            instance=queryset,
            many=True
        )
        return Response(data=result.data, status=200)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.prefetch_related('employee_set')
        return super(DepartmentViewSet, self).list(request, *args, **kwargs)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filter_class = filters.EmployeeFilter
