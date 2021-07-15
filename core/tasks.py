from celery import shared_task
from core import models
from django.utils.timezone import now


@shared_task(queue='default')
def create_file(state_id: int):
    with open(f'c:\\tmp\\states.txt', 'w+') as file:
        for n in range(1, 50001):
            print(n)
            file.write(f'state: {state_id}\n')


@shared_task(queue='default')
def create_customer_file():
    customers = models.Customer.objects.all()
    _now = now()
    with open(f"{_now.strftime('%Y%M%D%H%M%S')}-custumers.txt") as file:
        for c in customers:
            file.write(f'{c.name}\n')
