from django.urls import path,include
from .views import save_faculty   ,show_all_faculty, delete_all_faculty_records, faculty_login,faculty_info
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
      
      
      path('show_all_faculty/', show_all_faculty, name='show_all_faculty'),
      path('save_faculty/', save_faculty, name = 'save_faculty'),
      path('delete_all_faculty_records/', delete_all_faculty_records, name = 'delete_all_faculty_records'),
      path('faculty_login/', faculty_login, name = 'faculty_login'),
      path('faculty_info/<int:faculty_id>/',faculty_info, name='faculty_info'),
     




      path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]







