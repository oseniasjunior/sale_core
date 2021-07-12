from django.db import models


# Create your models here.
class ModelBase(models.Model):
    class Gender(models.TextChoices):
        MALE = ('M', 'Male')
        FEMALE = ('F', 'Female')

    id = models.AutoField(null=False, primary_key=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        managed = True
        abstract = True


class Supplier(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64)
    legal_document = models.CharField(null=False, blank=False, max_length=20)

    class Meta:
        db_table = 'supplier'


class ProductGroup(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)
    commission_percentage = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2)
    gain_percentage = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'product_group'


class Product(ModelBase):
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        db_column='id_product_group',
        null=False,
        blank=False
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        db_column='id_supplier',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)
    cost_price = models.DecimalField(null=False, blank=False, max_digits=16, decimal_places=2)
    sale_price = models.DecimalField(null=False, blank=False, max_digits=16, decimal_places=2)

    class Meta:
        db_table = 'product'


class State(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)
    abbreviation = models.CharField(null=False, blank=False, max_length=2)

    class Meta:
        db_table = 'state'


class City(ModelBase):
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64)

    class Meta:
        db_table = 'city'
        unique_together = [
            ('state', 'name',)
        ]


class Zone(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)

    class Meta:
        db_table = 'zone'


class District(ModelBase):
    city = models.ForeignKey(
        to='City',
        on_delete=models.DO_NOTHING,
        db_column='id_city',
        null=False,
        blank=False
    )
    zone = models.ForeignKey(
        to='Zone',
        on_delete=models.DO_NOTHING,
        db_column='id_zone',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64)

    class Meta:
        db_table = 'district'
        unique_together = [
            ('city', 'name',)
        ]


class Branch(ModelBase):
    distric = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64)

    class Meta:
        db_table = 'branch'


class MaritalStatus(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)

    class Meta:
        db_table = 'marital_status'


class Department(ModelBase):
    name = models.CharField(null=False, blank=False, max_length=64, unique=True)

    class Meta:
        db_table = 'department'


class Customer(ModelBase):
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        blank=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64)
    income = models.DecimalField(null=False, blank=False, max_digits=16, decimal_places=2)
    gender = models.CharField(null=False, blank=False, max_length=1, choices=ModelBase.Gender.choices)

    class Meta:
        db_table = 'customer'


class Employee(ModelBase):
    department = models.ForeignKey(
        to='Department',
        on_delete=models.DO_NOTHING,
        db_column='id_department',
        null=False,
        blank=False
    )
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False,
        blank=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False,
        blank=False
    )
    name = models.CharField(null=False, blank=False, max_length=64)
    salary = models.DecimalField(null=False, blank=False, max_digits=16, decimal_places=2)
    admission_date = models.DateField(null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    gender = models.CharField(null=False, blank=False, max_length=1, choices=ModelBase.Gender.choices)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f'{self.name} - {self.salary}'


class Sale(ModelBase):
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        db_column='id_customer',
        null=False,
        blank=False
    )
    branch = models.ForeignKey(
        to='Branch',
        on_delete=models.DO_NOTHING,
        db_column='id_branch',
        null=False,
        blank=False
    )
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_employee',
        null=False,
        blank=False
    )
    date = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        db_table = 'sale'


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False,
        blank=False
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        db_column='id_product',
        null=False,
        blank=False
    )
    quantity = models.DecimalField(null=False, blank=False, max_digits=16, decimal_places=3)

    class Meta:
        db_table = 'sale_item'
