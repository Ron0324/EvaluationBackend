# Generated by Django 5.0.1 on 2024-02-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0006_remove_faculty_last_name_alter_faculty_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
