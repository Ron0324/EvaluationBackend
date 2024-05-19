# Generated by Django 5.0.2 on 2024-05-01 05:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_faculty', '0016_evaluation_total_rate'),
        ('Departments', '0003_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultySubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departments.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departments.subject')),
            ],
            options={
                'unique_together': {('faculty', 'subject', 'semester')},
            },
        ),
    ]