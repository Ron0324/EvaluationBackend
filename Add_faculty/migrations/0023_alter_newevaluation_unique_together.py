# Generated by Django 5.0.2 on 2024-05-14 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0022_newevaluation_student'),
        ('Course_and_Students', '0005_alter_admin_username'),
        ('Departments', '0004_remove_semester_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='newevaluation',
            unique_together={('student', 'subject', 'semester', 'year')},
        ),
    ]