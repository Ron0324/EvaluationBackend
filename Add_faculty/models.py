from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Course_and_Students.models import Student
from Departments.models import Subject as DepartmentSubject
from Departments.models import Subject
from Course_and_Students.models import Admin


class FacultyManager(BaseUserManager):
    def create_user(self, id_number, password=None, **extra_fields):
        user = self.model(id_number=id_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id_number, password, **extra_fields)

class Faculty(AbstractBaseUser, PermissionsMixin):
    id_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)  
    last_name = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=128)
    selected_image = models.ImageField(upload_to='images/', blank=True, null=True, max_length=500)
    status = models.CharField(max_length=50)
    subjects = models.ManyToManyField(DepartmentSubject, related_name='faculties')

    # Required fields for AbstractBaseUser
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Additional fields
    is_staff = models.BooleanField(default=False)

    objects = FacultyManager()

    USERNAME_FIELD = 'id_number'

    # Add related_name to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='faculty_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='faculty_user_permissions')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class FacultySubject(models.Model):
    SEMESTER_CHOICES = (
        ('1', 'First'),
        ('2', 'Second'),
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(DepartmentSubject, on_delete=models.CASCADE)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    year = models.CharField(max_length=15,null=True)
   

    class Meta:
        unique_together = ('faculty', 'subject', 'semester', 'year')
    


class Evaluation(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    criteria_A = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_B = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_C = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_D = models.DecimalField(max_digits=5, decimal_places=2)
    total_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    feedback = models.TextField()

    class Meta:
        db_table = 'Evaluation'
class newEvaluation(models.Model):
    SEMESTER_CHOICES = (
        ('1', 'First'),
        ('2', 'Second'),
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    student_id_number =models.CharField(max_length=15, null=True)
    admin_id_number =models.CharField(max_length=15, null=True)
    course =models.CharField(max_length=15, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)  # Change ForeignKey to CharField
    year_level=models.CharField(max_length=15, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)
    year = models.CharField(max_length=15)
    criteria_A = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_B = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_C = models.DecimalField(max_digits=5, decimal_places=2)
    criteria_D = models.DecimalField(max_digits=5, decimal_places=2)
    total_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    feedback = models.TextField()

    class Meta:
        db_table = 'Subjects_Evaluation'
        unique_together = ('student','admin', 'subject', 'semester', 'year')


    def __str__(self):
        return f"Evaluation for {self.faculty} - {self.subject} - Semester {self.semester} {self.year}"