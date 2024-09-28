from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')

    # Изменяем related_name для групп и разрешений, чтобы избежать конфликта
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='inventory_user_set',  # Здесь меняем related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='inventory_user_permissions',  # И здесь
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Warehouse(models.Model):
    name = models.CharField(max_length=255,unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, related_name='products', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name