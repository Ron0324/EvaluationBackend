from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_criteria,save_evaluation_date

urlpatterns = [
  
     path('show_criteria/', show_criteria, name='show_criteria'),
     path('save_evaluation_date/', save_evaluation_date, name='save_evaluation_date'),
     
     
]  