# Generated by Django 5.1.1 on 2024-09-27 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_warehouse_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.warehouse'),
        ),
    ]
