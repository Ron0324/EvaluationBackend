from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import save_course,show_courses,create_student,show_Students,student_login,create_admin,admin_login,show_admins,admin_update,admin_delete

urlpatterns = [
  
     path('save_course/', save_course, name='save_course'),
     path('show_courses/', show_courses, name='show_courses'),
     path('create_students/', create_student,name='create_students'),
     path('show_Students/', show_Students,name='show_Students'),
     path('student_login/', student_login,name='student_login'),
     path('create_admin/', create_admin,name='create_admin'),
     path('admin_login/', admin_login,name='admin_login'),
     path('show_admins/', show_admins,name='show_admins'),
     path('admin_update/', admin_update,name='admin_update'),
     path('admin_delete/<int:admin_id>/', admin_delete,name='admin_delete'),
       
     
     
]  

