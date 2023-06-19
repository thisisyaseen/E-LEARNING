from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    otp_code = models.CharField(max_length=6)
    subscribed_courses = models.ManyToManyField('teachers.Course', related_name='subscribed_students')
