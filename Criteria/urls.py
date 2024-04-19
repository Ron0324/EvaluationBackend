from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_criteria,save_evaluation_date,get_evaluation_dates,update_evaluation_date

urlpatterns = [
  
     path('show_criteria/', show_criteria, name='show_criteria'),
     path('save_evaluation_date/', save_evaluation_date, name='save_evaluation_date'),
     path('get_evaluation_dates/', get_evaluation_dates, name='get_evaluation_dates'),
     path('update_evaluation_date/', update_evaluation_date, name='update_evaluation_date'),


     
     
]  