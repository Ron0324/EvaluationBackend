# Generated by Django 5.0.2 on 2024-05-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0023_alter_newevaluation_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newevaluation',
            name='year',
            field=models.CharField(max_length=15),
        ),
    ]
