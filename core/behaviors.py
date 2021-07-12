from core import models


class QuantityEmployeeByDistrictBehavior:

    def get_districts(self):
        return models.District.objects.all()

    def execute(self):
        districts = models.District.objects.all()
        for distric in districts:
            counter = models.Employee.objects.filter(district=distric).count()
            print(f'{distric.name} - {counter}')


class GenerateScriptAlterSequenceBehavior:

    def __init__(self):
        self.ids = {}
        self.path = 'c:\\tmp\\script.sql'

    def max_id_models(self):
        self.ids['branch'] = models.Branch.objects.order_by('id').last().id
        self.ids['city'] = models.City.objects.order_by('id').last().id
        self.ids['customer'] = models.Customer.objects.order_by('id').last().id
        self.ids['department'] = models.Department.objects.order_by('id').last().id
        self.ids['district'] = models.District.objects.order_by('id').last().id
        self.ids['employee'] = models.Employee.objects.order_by('id').last().id
        self.ids['marital_status'] = models.MaritalStatus.objects.order_by('id').last().id
        self.ids['product'] = models.Product.objects.order_by('id').last().id
        self.ids['product_group'] = models.ProductGroup.objects.order_by('id').last().id
        self.ids['sale'] = models.Sale.objects.order_by('id').last().id
        self.ids['sale_item'] = models.SaleItem.objects.order_by('id').last().id
        self.ids['state'] = models.State.objects.order_by('id').last().id
        self.ids['supplier'] = models.Supplier.objects.order_by('id').last().id
        self.ids['zone'] = models.Zone.objects.order_by('id').last().id

    def save_file(self):
        with open(self.path, 'w+') as file:
            for key, value in self.ids.items():
                file.write(f"ALTER SEQUENCE {key}_id_seq RESTART {value + 1};\n")

    def execute(self):
        self.max_id_models()
        self.save_file()
