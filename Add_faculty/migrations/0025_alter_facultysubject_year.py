# Generated by Django 5.0.2 on 2024-05-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0024_alter_newevaluation_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultysubject',
            name='year',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
