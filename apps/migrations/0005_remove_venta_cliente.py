# Generated by Django 5.0.4 on 2024-05-31 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_factura_numerof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='cliente',
        ),
    ]