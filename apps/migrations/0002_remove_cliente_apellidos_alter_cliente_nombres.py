# Generated by Django 5.0.4 on 2024-05-31 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='apellidos',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombres',
            field=models.CharField(max_length=150),
        ),
    ]