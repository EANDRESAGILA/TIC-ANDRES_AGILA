# Generated by Django 5.0.4 on 2024-04-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=50)),
                ('apeliidos', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=45)),
                ('celular', models.IntegerField()),
            ],
        ),
    ]
