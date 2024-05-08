#Departments models

from django.db import models


class Departments(models.Model):
    CodeName = models.CharField(max_length=20,unique=True,null=False, blank=False)
    Descriptions = models.CharField(max_length=100, unique=True,null=False, blank=False)

    def __str__(self):
        return self.CodeName
    class Meta:
        db_table = 'Departments'


 

class Subject(models.Model):
    Subname = models.CharField(max_length=20,null=False, blank=False)
    SubDescriptions  =  models.CharField(max_length=100,null=False, blank=False)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.Subname


class Semester(models.Model):
    SEMESTER_CHOICES = (
        ('1', 'First'),
        ('2', 'Second'),
    )
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

    def __str__(self):
        return self.get_semester_display()
    


