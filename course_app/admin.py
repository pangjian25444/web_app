from django.contrib import admin
from .models import *
# Register your models here.
app_name = 'course_app'

admin.site.register(ClassName)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(CourseANDSubject)
admin.site.register(Course)
admin.site.register(ClassTimeTable)