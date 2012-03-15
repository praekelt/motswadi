from django.contrib import admin
from motswadi.models import Event, Guardian, NonAttendance, School, Student, \
        Subject, SubjectResult, Teacher, Test, TestResult

admin.site.register(Event)
admin.site.register(Guardian)
admin.site.register(NonAttendance)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SubjectResult)
admin.site.register(Teacher)
admin.site.register(Test)
admin.site.register(TestResult)
