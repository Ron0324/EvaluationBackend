from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number}) - {self.course}"

    class Meta:
        db_table = 'students'

class Admin(AbstractUser):
    full_name = models.CharField(max_length=150, unique=False) 
    id_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.full_name} ({self.id_number})"

    class Meta:
        db_table = 'admins'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='admin_set',  # Change related_name to avoid clash
        related_query_name='admin',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='admin_set',  # Change related_name to avoid clash
        related_query_name='admin',
    )