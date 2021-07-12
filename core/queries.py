from django.db.models.expressions import RawSQL

from core import models
from django.db.models import Q, Value, ExpressionWrapper, FloatField, F, Case, When, CharField, Sum, Avg, Max, Min, \
    Count, OuterRef, Subquery, Exists
from django.db.models.functions import Cast, LPad, Lower, Upper, StrIndex, Extract, Concat, Replace, Substr, Trim, \
    Coalesce


def ranking_employee():
    return models.Employee.objects.order_by('-salary')[:5]


def ranking_employee_with_values():
    return models.Employee.objects.order_by('-salary').values('name', 'salary')[:5]


def employee_female():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE)


def employee_female_and_salary_5000():
    return models.Employee.objects.filter(
        gender=models.ModelBase.Gender.FEMALE,
        salary=5000
    )


def employee_female_and_salary_5000_or():
    return models.Employee.objects.filter(
        Q(gender=models.ModelBase.Gender.FEMALE) | Q(salary=5000)
    )


def employee_female_gte_500():
    return models.Employee.objects.filter(
        Q(gender=models.ModelBase.Gender.FEMALE) | Q(salary__gte=5000)
    )


def customer_between_5000_1000_a():
    return models.Customer.objects.filter(
        Q(income__gte=5000) & Q(income__lte=10000)
    )


def customer_between_5000_1000_b():
    return models.Customer.objects.filter(income__gte=5000, income__lte=10000)


def customer_between_5000_1000_c():
    return models.Customer.objects.filter(income__range=(5000, 10000))


def customer_between_5000_1000_exclude():
    return models.Customer.objects.exclude(
        income__range=(5000, 10000)
    ).filter(gender=models.ModelBase.Gender.FEMALE)


def get_department_by_id(pk: int):
    try:
        return models.Department.objects.get(pk=pk)
    except models.Department.DoesNotExist:
        print('Department not found')


def query02():
    queryset = models.Department.objects.annotate(
        company=Value('Sidia')
    ).values('id', 'name', 'company')
    return queryset


def query03():
    new_salary = ExpressionWrapper(F('salary') + Value(100), output_field=FloatField())

    queryset = models.Employee.objects.annotate(
        new_salary=new_salary
    ).values('name', 'salary', 'new_salary')
    return queryset


def query04():
    queryset = models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.FEMALE, then=Value('Female')),
            default=Value('Male'),
            output_field=CharField()
        )
    ).values('name', 'gender_description')
    return queryset


def query_case_tag():
    qs = models.Employee.objects.annotate(
        tipo=Case(
            When(Q(salary__lte=2000), then=Value('Estagiário')),
            When(Q(salary__gt=2000) & Q(salary__lte=3000), then=Value('Jr')),
            When(Q(salary__gt=3000) & Q(salary__lte=6000), then=Value('Pleno')),
            When(Q(salary__gt=6000), then=Value('Senior')),
            output_field=CharField()
        )
    ).values('name', 'salary', 'tipo')
    return qs


def query_case_tag_range():
    qs = models.Employee.objects.annotate(
        tipo=Case(
            When(salary__lte=2000, then=Value('Estagiário')),
            When(salary__range=(2000, 3000), then=Value('Jr')),
            When(salary__range=(3001, 6000), then=Value('Pleno')),
            When(salary__gt=6000, then=Value('Senior')),
            output_field=CharField()
        )
    ).values('name', 'salary', 'tipo')
    return qs


def query05():
    queryset = models.Employee.objects.filter(department__name__icontains='tec').values(
        'name', 'department__name', 'district__name'
    )
    return queryset


def query06():
    queryset = models.Department.objects.filter(
        employee__salary__lte=3000
    ).values('id', 'name')
    return queryset


def query07():
    text_code = Cast(F('id'), output_field=CharField())
    upper_name = Upper('name')
    lower_name = Lower('name')
    index = StrIndex(F('name'), Value(' '))
    month = Extract('created_at', 'month')
    day = Extract('created_at', 'day')
    custom_name = Concat('name', Value(' - '), 'department__name')

    queryset = models.Employee.objects.annotate(
        custom_code=LPad(text_code, 5, Value('0')),
        upper_name=upper_name,
        lower_name=lower_name,
        index=index,
        month=month,
        day=day,
        custom_name=custom_name
    ).values('id', 'custom_code', 'name', 'upper_name', 'lower_name', 'index', 'month', 'day', 'custom_name')
    return queryset


def query08():
    name_replace = Replace(F('name'), Value('Srta.'), Value(''))
    name_replace = Replace(name_replace, Value('Sr.'), Value(''))
    name_replace = Replace(name_replace, Value('Sra.'), Value(''))
    name_replace = Replace(name_replace, Value('Dr.'), Value(''))
    name_replace = Trim(name_replace)
    index_space = StrIndex(name_replace, Value(' '))

    queryset = models.Customer.objects.annotate(
        first_name=Trim(Substr(name_replace, 1, index_space)),
        _age=RawSQL("select fn_hellow_world()", ())
    ).values('first_name', '_age')
    return queryset


def total_salary_by_gender():
    queryset = models.Employee.objects.values('gender').annotate(
        total=Sum('salary')
    ).values('gender', 'total')
    return queryset


def total_income_by_zone():
    qs = models.Customer.objects.values('district__zone__name').annotate(
        average=Avg('income')
    ).values('district__zone__name', 'average')
    return qs


def total_employee_by_zone():
    qs = models.Employee.objects.values('district__zone__name').annotate(
        count=Count('id')
    ).values('district__zone__name', 'count')
    return qs


def ranking_sale_by_quantity_and_zone():
    qs = models.Sale.objects.values('customer__district__zone__name').annotate(
        total=Coalesce(Sum('saleitem__quantity'), Value(0), output_field=FloatField())
    ).order_by('-total').values('customer__district__zone__name', 'total')
    return qs


def last_sale_product():
    subquery = models.SaleItem.objects.filter(product=OuterRef('id')).order_by('-sale__date').values('sale__date')[:1]
    queryset = models.Product.objects.annotate(
        last_sale=Subquery(subquery)
    ).values('name', 'last_sale')
    return queryset


def query09():
    subquery = models.Sale.objects.filter(employee=OuterRef('id'))
    queryset = models.Employee.objects.annotate(
        exists_sale=Exists(subquery)
    ).values('name', 'exists_sale')
    return queryset


def query10():
    subquery = models.SaleItem.objects.values_list('id', flat=True).distinct()
    queryset = models.Product.objects.filter(id__in=subquery)
    return queryset


def employee_by_department():
    queryset = models.Department.objects.values('name').annotate(
        counter=Count('employee__id')
    ).values('name', 'counter')
    return queryset
