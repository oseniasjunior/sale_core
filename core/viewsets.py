from rest_framework import viewsets
from rest_framework.decorators import action
from core import models, serializers


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer

    @action(detail=False, methods=['GET'])
    def get_by_name(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        self.queryset = models.State.objects.filter(name__icontains=name)
        return super(StateViewSet, self).list(request, *args, **kwargs)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
