from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Student Authentication
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    
    # Student Portal
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/enrollment/', views.course_enrollment, name='course_enrollment'),
    path('student/routine/', views.student_routine, name='student_routine'),
    
    # AJAX Endpoints
    path('student/ajax/enroll/', views.ajax_enroll_course, name='ajax_enroll_course'),
]