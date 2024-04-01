from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from Departments.models import Subject as DepartmentSubject

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
