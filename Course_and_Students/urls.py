from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import save_course,show_courses,create_student,show_Students,student_login

urlpatterns = [
  
     path('save_course/', save_course, name='save_course'),
     path('show_courses/', show_courses, name='show_courses'),
     path('create_students/', create_student,name='create_students'),
     path('show_Students/', show_Students,name='show_Students'),
     path('student_login/', student_login,name='student_login'),
     
]  

