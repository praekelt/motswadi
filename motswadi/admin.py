from django.contrib import admin
from motswadi.models import Guardian, NonAttendance, School, Student, Subject, SubjectResult, Test, TestResult

admin.site.register(Guardian)
admin.site.register(NonAttendance)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SubjectResult)
admin.site.register(Test)
admin.site.register(TestResult)
