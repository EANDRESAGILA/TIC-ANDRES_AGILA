# Generated by Django 5.0.4 on 2024-06-06 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_alter_factura_iva_alter_factura_subtotal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='factura',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='factura',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='venta',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='venta',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
