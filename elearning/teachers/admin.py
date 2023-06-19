from django.contrib import admin
from .models import Teacher, Course

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'title', 'price')
    search_fields = ('teacher__username', 'title')
    list_filter = ('teacher',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(teacher=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.teacher:
            obj.teacher = request.user
        obj.save()
