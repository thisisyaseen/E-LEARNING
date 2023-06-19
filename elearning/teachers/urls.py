from django.urls import path
from teachers.views import  SubscribedStudentsView, TeacherLoginView, TeacherRegistrationView,TeacherDashboardView, TeacherRedirectView, Course
from teachers import views
urlpatterns = [
    path('login/', TeacherLoginView.as_view(), name='teacher-login'),
    path('register/', TeacherRegistrationView.as_view(), name='teacher-registration'),
    path('dashboard/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('redirect/', TeacherRedirectView.as_view(), name='teacher-redirect'),
    path('dashboard/subscribed-students/<int:course_id>/', views.SubscribedStudentsView.as_view(), name='subscribed-students'),
]

