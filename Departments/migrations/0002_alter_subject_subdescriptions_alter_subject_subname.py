# Generated by Django 5.0.1 on 2024-02-15 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Departments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='SubDescriptions',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subject',
            name='Subname',
            field=models.CharField(max_length=20),
        ),
    ]
