from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from students.models import Student
from teachers.models import Course
import random
from django.core.mail import send_mail
from django.conf import settings

class StudentLoginView(APIView):
    def get(self, request):
        return render(request, 'student_login.html')
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        otp_code = request.data.get('otp_code')

        student = Student.objects.filter(username=username, password=password, otp_code=otp_code).first()

        if student:
            return redirect('student-dashboard')
        else:
            return Response({'message': 'Invalid credentials.'})

class OTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = generate_otp()
        send_otp_email(email, otp_code)
        return Response({'message': 'OTP sent successfully.'})
    
class StudentRegistrationView(APIView):
    def get(self, request):
        return render(request, 'student_register.html')

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        otp_code = generate_otp()

       
        student = Student.objects.create(username=username, email=email, password=password, otp_code=otp_code)

        
        send_otp_email(email, otp_code)

        return redirect('student-login')

class StudentDashboardView(APIView):
    def get(self, request):
        student_id = request.user.id  
        student = Student.objects.get(id=student_id)
        subscribed_courses = student.subscribed_courses.all()
        all_courses = Course.objects.all()

        course_list = []
        for course in subscribed_courses:
            course_data = {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'price': course.price
            }
            course_list.append(course_data)

        context = {'courses': course_list, 'all_courses': all_courses}
        return render(request, 'student_dashboard.html', context)

    def post(self, request):
        student_id = request.user.id
        action = request.POST.get('action')

        if action == 'search':
            query = request.POST.get('query')
            courses = Course.objects.filter(title__icontains=query)
            course_list = [{'id': course.id, 'title': course.title, 'description': course.description} for course in courses]
            return render(request, 'student_dashboard.html', {'search_results': course_list})

        elif action == 'subscribe':
            course_id = request.POST.get('course_id')
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            student.subscribed_courses.add(course)
            return redirect('student-dashboard')

        elif action == 'unsubscribe':
            course_id = request.POST.get('course_id')
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            student.subscribed_courses.remove(course)
            return redirect('student-dashboard')

        return redirect('student-dashboard')

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(email, otp_code):
    send_mail(
        'OTP Verification',
        f'Your OTP code: {otp_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
