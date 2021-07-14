from django_filters import filterset, widgets
from core import models
from django.db.models import Q


class CharInFilter(filterset.BaseInFilter):
    pass


class StateFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    abbreviation = filterset.CharFilter(lookup_expr='iexact')
    name_or_abbreviation = filterset.CharFilter(method='filter_name_or_abbreviation')
    city = filterset.CharFilter(method='filter_city')

    def filter_name_or_abbreviation(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(abbreviation__icontains=value))

    def filter_city(self, queryset, name, value):
        return queryset.filter(city__name__icontains=value)

    class Meta:
        model = models.State
        fields = ['name', 'abbreviation', 'name_or_abbreviation', 'city']


class EmployeeFilter(filterset.FilterSet):
    start_salary = filterset.NumberFilter(lookup_expr='gte', field_name='salary')
    end_salary = filterset.NumberFilter(lookup_expr='lte', field_name='salary')
    gender = CharInFilter(lookup_expr='in')
    active = filterset.BooleanFilter(widget=widgets.BooleanWidget)

    class Meta:
        model = models.Employee
        fields = ['start_salary', 'end_salary', 'gender', 'active']
