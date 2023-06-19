from django.shortcuts import redirect, get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from teachers.models import Teacher
from django.core.mail import send_mail
from django.conf import settings
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from teachers.models import Teacher, Course
from django.shortcuts import render

class TeacherRegistrationView(APIView):
    def get(self, request):
        return render(request, 'teachers_register.html')
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        otp_code = generate_otp()
        teacher = Teacher.objects.create(username=username, email=email, password=password, otp_code=otp_code)
        send_otp_email(email, otp_code)
        return redirect('teacher-login')

class TeacherLoginView(APIView):
    def get(self, request):
        return render(request, 'teachers_login.html')
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        otp_code = request.data.get('otp_code')
        teacher = Teacher.objects.filter(username=username, password=password, otp_code=otp_code).first()

        if teacher:
            return Response({'message': 'Teacher login successful.'})
        else:
            return Response({'message': 'Invalid credentials.'})

class TeacherRedirectView(APIView):
    def get(self, request):
        return redirect('teacher-login')
    
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp_code):
    subject = 'OTP Code for E-Learning Platform'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

class OTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = generate_otp()
        send_otp_email(email, otp_code)
        return Response({'message': 'OTP sent successfully.'})
    


class TeacherDashboardView(APIView):
    def get(self, request):
        teacher_id = request.user.id
        teacher = get_object_or_404(Teacher, id=teacher_id)
        courses = teacher.courses.all()

        course_list = []
        for course in courses:
            subscribed_students = course.subscribed_students.all()
            subscribed_students_list = [student.username for student in subscribed_students]

            course_data = {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'price': course.price,
                'subscribed_students': subscribed_students_list,
            }
            course_list.append(course_data)

        context = {'courses': course_list}
        return render(request, 'teachers_dashboard.html', context)

    def post(self, request):
        teacher_id = request.user.id
        action = request.POST.get('action')  

        if action == 'create':
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')

            teacher = get_object_or_404(Teacher, id=teacher_id)
            course = Course.objects.create(teacher=teacher, title=title, description=description, price=price)

            
            courses = teacher.courses.all()
            course_list = []
            for course in courses:
                course_data = {
                    'id': course.id,
                    'title': course.title,
                    'description': course.description,
                    'price': course.price
                }
                course_list.append(course_data)

            context = {'courses': course_list}
            return render(request, 'teachers_dashboard.html', context)

        elif action == 'edit':
            course_id = request.POST.get('course_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')

            course = get_object_or_404(Course, id=course_id)
            course.title = title
            course.description = description
            course.price = price
            course.save()

        elif action == 'delete':
            course_id = request.POST.get('course_id')
            course = get_object_or_404(Course, id=course_id)
            course.delete()

        return redirect('teacher-dashboard')
    
class SubscribedStudentsView(APIView):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        subscribed_students = course.subscribed_students.all()
        students = [{'username': student.username, 'email': student.email} for student in subscribed_students]
        return Response({'students': students})