from django.contrib import admin
from motswadi.models import AssessmentResult, School, Student, Subject, Teacher


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'student', 'percentage')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school', 'grade', 'class_teacher', )
    list_filter = ('school', 'grade', 'class_teacher', )


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'school',)
    list_filter = ('school',)

admin.site.register(AssessmentResult, AssessmentAdmin)
admin.site.register(School)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
