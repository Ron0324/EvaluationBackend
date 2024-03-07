from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_criteria

urlpatterns = [
  
     path('show_criteria/', show_criteria, name='show_criteria'),

     
]  