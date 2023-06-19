from django.urls import path
from students.views import StudentLoginView, StudentRegistrationView,StudentDashboardView

urlpatterns = [
    path('login/', StudentLoginView.as_view(), name='student-login'),
    path('register/', StudentRegistrationView.as_view(), name='student-registration'),
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
]
