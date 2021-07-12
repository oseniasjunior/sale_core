from django_filters import filterset, widgets

from core import models


class StateFilter(filterset.FilterSet):
    active = filterset.BooleanFilter(widget=widgets.BooleanWidget)

    class Meta:
        model = models.State
        fields = ['active']


class NumberInFilter(filterset.BaseInFilter):
    pass


class EmployeeFilter(filterset.FilterSet):
    start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    end_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')
    salary = NumberInFilter(lookup_expr='in')

    class Meta:
        model = models.Employee
        fields = ['start_salary', 'end_salary', 'salary']
