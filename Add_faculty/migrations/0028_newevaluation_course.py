# Generated by Django 5.0.2 on 2024-05-19 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0027_newevaluation_admin_id_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newevaluation',
            name='course',
            field=models.CharField(max_length=15, null=True),
        ),
    ]