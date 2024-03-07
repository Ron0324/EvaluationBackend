from django.db import models
from django.contrib.auth.models import AbstractUser

class Course(models.Model):
    description = models.CharField(max_length=255)
    course_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'Course'


class Student(AbstractUser):
    username = models.CharField(max_length=150, unique=False) 
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    course = models.CharField(max_length=100)
      # Use an appropriate max length for your course names
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number}) - {self.course}"

    class Meta:
        db_table = 'students'
    