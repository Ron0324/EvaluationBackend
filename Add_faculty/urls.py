from django.urls import path,include
from .views import admin_save_evaluation,calculate_averages, save_faculty, get_years,fetch_subjects,fetch_evaluations, faculty_subjects,save_faculty_subjects,add_subjects_to_faculty  ,show_all_faculty, delete_all_faculty_records, faculty_login,faculty_info,save_evaluation,evaluation_score_per_faculty,analyze_feedback
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
      
      
      path('show_all_faculty/', show_all_faculty, name='show_all_faculty'),
      path('save_faculty/', save_faculty, name = 'save_faculty'),
      path('delete_all_faculty_records/', delete_all_faculty_records, name = 'delete_all_faculty_records'),
      path('faculty_login/', faculty_login, name = 'faculty_login'),
      path('add_subjects_to_faculty/', add_subjects_to_faculty, name = 'add_subjects_to_faculty'),
      path('faculty/<int:faculty_id>/subjects/<str:year>/<int:semester>/', faculty_subjects, name='faculty_subjects'),
       path('fetch_subjects/<int:faculty_id>/<str:year>/<int:semester>/', fetch_subjects, name='fetch_subjects'),
       path('fetch-evaluations/<int:faculty_id>/<int:subject_id>/<str:year>/<int:semester>/', fetch_evaluations, name='fetch_evaluations'),
       path('save_evaluation/<int:faculty_id>/',admin_save_evaluation, name='admin_save_evaluation'),
       path('calculate_averages/<int:faculty_id>/', calculate_averages, name = 'calculate_averages'),



      path('faculty_info/<int:faculty_id>/',faculty_info, name='faculty_info'),
      path('save-evaluation/<int:faculty_id>/',save_evaluation, name='save_evaluation'),
      path('save_faculty_subjects/<int:faculty_id>/', save_faculty_subjects, name='save_faculty_subjects'),
      path('evaluation_score_per_faculty/<int:faculty_id>/', evaluation_score_per_faculty, name='evaluation_score_per_faculty'),
      path('analyze-feedback/<int:faculty_id>/<int:subject_id>/<str:year>/<int:semester>/', analyze_feedback, name='analyze_feedback'),
       path('get_years/<int:faculty_id>/', get_years, name='get_years'),
     


     




      path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]







