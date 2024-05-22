# Generated by Django 5.0.4 on 2024-05-10 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_clientes_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('codigo_producto', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_articulo', models.CharField(max_length=100)),
                ('unidades', models.IntegerField()),
            ],
            options={
                'db_table': 'tabla_Inventario',
            },
        ),
        migrations.CreateModel(
            name='Precios',
            fields=[
                ('articulo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='apps.inventario')),
                ('precio_neto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'tabla_Precios',
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.IntegerField()),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.inventario')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.clientes')),
            ],
            options={
                'db_table': 'tabla_Ventas',
            },
        ),
    ]
