from django.urls import path
from .views import DepartmentListAPIView,save_department,show_departments,show_subjects, save_multiple_subjects,show_subjects_by_department
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('api/save_multiple_subjects/<int:department_id>/', save_multiple_subjects, name='save_multiple_subjects'),
     path('api/save_department/', save_department, name='save_department'),
     path('show_departments/', show_departments, name='show_departments'),
     path('show_subjects/', show_subjects, name = 'show_subjects'),
     path('show_subjects_by_department/<int:department_id>/', show_subjects_by_department, name='show_subjects_by_department'),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    