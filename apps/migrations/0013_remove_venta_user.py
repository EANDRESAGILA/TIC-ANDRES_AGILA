# Generated by Django 5.0.4 on 2024-06-26 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_factura_user_producto_user_venta_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='user',
        ),
    ]
