# Generated by Django 5.0.2 on 2024-03-03 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('course_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Course',
            },
        ),
    ]
