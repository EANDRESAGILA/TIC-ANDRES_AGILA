# Generated by Django 5.0.4 on 2024-05-31 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_remove_cliente_apellidos_alter_cliente_nombres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='forma_pago',
            new_name='formaPago',
        ),
    ]
