# Initialize Django ENV.
from django.core.management import setup_environ
from motswadi import settings
setup_environ(settings)

from motswadi.models import Student, Teacher
from worker import DynamicMenuApplicationWorker, DynamicMenu


class AttendanceMenu(DynamicMenu):
    """
    Resnpnds with attendance history for given student.
    """
    options = [
        ('Back', {}, 'StudentMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Attendance record for %s:\nAbsent - %s days." % \
                (student.name, student.nonattendance_set.count())


class DatesMenu(DynamicMenu):
    """
    Responds with important dates for given student.
    """
    options = [
        ('Back', {}, 'StudentMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Important dates for %s:\n%s" % (student.name, '\n'.join(\
                ['%s - %s' % (event.title, event.date) \
                for event in student.event_set.all()]))


class TeacherInfoMenu(DynamicMenu):
    """
    Responds with information about given teacher.
    """
    options = [
        ('Back', {}, 'TeacherMenu')
    ]

    def get_text(self):
        teacher = Teacher.objects.get(pk=self.session['teacher_pk'])
        return "Information for %s:\nContact Number - %s" % \
                (teacher.name, teacher.contact_number)


class TeacherMenu(DynamicMenu):
    """
    Menu listing various teachers for given student.
    """
    options = [
        ('Back', {}, 'StudentMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Teacher information for %s:" % student

    def get_options(self):
        teachers = Student.objects.get(pk=self.session['student_pk']).\
                teacher_set.all()
        return [('%s - %s' % (teacher.subject.title, teacher.name), \
                {'teacher_pk': teacher.pk}, 'TeacherInfoMenu') \
                for idx, teacher in enumerate(teachers)] + self.options


class TestResultsMenu(DynamicMenu):
    """
    Responds with latest test results for given student.
    """
    options = [
        ('Back', {}, 'StudentMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Latest tests results for %s:\n%s" % (student.name, '\n'.join(\
                ['%s - %s (%s) - %s%%' % (result.test.subject.title, \
                result.test.title, result.test.date, result.percentage) \
                for result in student.testresult_set.all()[:5]]))


class StudentMenu(DynamicMenu):
    """
    Menu listing various report options for given student.
    """
    options = [
        ('Attendance.', {}, 'AttendanceMenu'),
        ('Subject marks.', {}, 'SubjectMarksMenu'),
        ('Test results.', {}, 'TestResultsMenu'),
        ('Important dates.', {}, 'DatesMenu'),
        ('Teacher information.', {}, 'TeacherMenu'),
        ('Back', {}, 'WelcomeMenu')
    ]
    
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Report choices for %s." % student


class SubjectMarksMenu(DynamicMenu):
    """
    Responds with subject marks for given student.
    """
    options = [
        ('Back', {}, 'StudentMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Subject marks for %s:\n%s" % (student.name, '\n'.join(\
                ['%s - %s%%' % (result.subject.title, result.percentage) \
                for result in student.subjectresult_set.all()]))


class WelcomeMenu(DynamicMenu):
    """
    Initial welcome/geteway landing menu.
    """
    text = 'Welcome to Motswadi. Select a student.'

    def get_options(self):
        students = Student.objects.all()
        return [(student.name, {'student_pk': student.pk}, 'StudentMenu') \
                for idx, student in enumerate(students)]


class MotswadiApplicationWorker(DynamicMenuApplicationWorker):
    """
    Main Motswadi application worker responsible for
    menu navigation and info replies.
    """
    initial_menu = WelcomeMenu
