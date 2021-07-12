from django.db.models.signals import post_save
from django.dispatch import receiver
from core import models


# @receiver(post_save, sender=models.State, dispatch_uid='create_file')
# def create_file(**kwargs):
#     instance: models.State = kwargs.get('instance')
#     with open(f'c:\\tmp\\{instance.id}', 'w+') as file:
#         file.write(f'{instance.name} - {instance.abbreviation}')
