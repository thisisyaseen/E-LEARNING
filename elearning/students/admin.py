from django.contrib import admin
from students.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  
    search_fields = ('username', 'email') 
    list_filter = ('subscribed_courses',)  
admin.site.register(Student, StudentAdmin)
