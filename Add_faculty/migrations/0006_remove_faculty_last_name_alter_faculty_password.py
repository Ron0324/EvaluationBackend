# Generated by Django 5.0.1 on 2024-02-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0005_remove_faculty_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='faculty',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
