# Generated by Django 5.0.4 on 2024-06-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_remove_venta_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
