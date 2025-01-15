from django.contrib import admin

# Register your models here.
from .models import Course, CourseMember, CourseContent, Comment

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseMember)
admin.site.register(CourseContent)
admin.site.register(Comment)