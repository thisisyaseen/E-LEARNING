from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from students.views import StudentRegistrationView,  StudentDashboardView, StudentLoginView, OTPVerificationView
from teachers.views import TeacherRegistrationView , TeacherLoginView, TeacherDashboardView, SubscribedStudentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/students/', include('students.urls')),
    path('api/teachers/', include('teachers.urls')),
    path('students/register/', StudentRegistrationView.as_view(), name='student-register'),
    path('teachers/register/', TeacherRegistrationView.as_view(), name='teacher-register'),
    path('students/dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('teachers/dashboard/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('courses/<int:course_id>/students/', SubscribedStudentsView.as_view(), name='subscribed-students'),
    
    path('students/login/', StudentLoginView.as_view(), name='student-login'),
    path('teachers/login/', TeacherLoginView.as_view(), name='teacher-login'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp-verification'),
    path('', TemplateView.as_view(template_name='student_login.html'), name='home'),
]
