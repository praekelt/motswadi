from datetime import date, timedelta

# Initialize Django ENV.
from django.core.management import setup_environ
from motswadi import settings
setup_environ(settings)

from motswadi.models import Student, Subject
from worker import DynamicMenuApplicationWorker, DynamicMenu


class AttendanceMenu(DynamicMenu):
    """
    Resnpnds with attendance history for given student.
    """
    options = [
        ('Back', {}, 'motswadi.application.StudentMenu'),
        ('Main Menu', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        absent_today = bool(student.nonattendance_set.filter(\
                date=date.today()).count())
        absent_count = student.nonattendance_set.filter(\
                date__gte=date.today() - timedelta(days=30)).count()
        return '-Attendance-\n%s is %sat school today.\n%s has been absent '\
                '%s day%s out of the last 30 days.' % \
                (student, "not " if absent_today else "", student, \
                absent_count, "" if absent_count == 1 else "s")


class DatesMenu(DynamicMenu):
    """
    Responds with important dates for given student.
    """
    options = [
        ('Back', {}, 'motswadi.application.StudentMenu'),
        ('Main Menu', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "-Important dates-\n%s" % ('\n'.join(['%s: %s' % \
                (event.date.strftime("%d %b"), event.title) \
                for event in student.event_set.all()]))


class TeacherInfoMenu(DynamicMenu):
    """
    Responds with information about student class teacher.
    """
    options = [
        ('Back', {}, 'motswadi.application.StudentMenu'),
        ('Main Menu', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        teacher = student.class_teacher
        return '-Teacher Information-\n%s\nContact Number: %s\nPlease feel '\
                'free to contact.' % (teacher, teacher.contact_number)


class SubjectProgressMenu(DynamicMenu):
    """
    Responds with subject progress results for given student.
    """
    options = [
        ('Back', {}, 'motswadi.application.AcademicProgressMenu'),
        ('Main Menu', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        subject = Subject.objects.get(pk=self.session['subject_pk'])
        return "-Academic progress-\n%s results for %s.\n%s" % \
                (subject, student, '\n'.join(['%s: %s%%' % \
                (result.title, result.percentage) for result in \
                student.assessmentresult_set.filter(subject=subject)]))


class StudentMenu(DynamicMenu):
    """
    Menu listing various report options for given student.
    """
    options = [
        ('Attendance.', {}, 'motswadi.application.AttendanceMenu'),
        ('Academic progress.', {}, \
                'motswadi.application.AcademicProgressMenu'),
        ('Important dates.', {}, 'motswadi.application.DatesMenu'),
        ('Teacher information.', {}, 'motswadi.application.TeacherInfoMenu'),
        ('Back', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "What would you like to view for %s?" % student


class AcademicProgressMenu(DynamicMenu):
    """
    Responds with subject marks for given student.
    """
    options = [
        ('Back', {}, 'motswadi.application.StudentMenu'),
        ('Main Menu', {}, 'motswadi.application.WelcomeMenu')
    ]

    def get_text(self):
        return "-Academic progress-\nWhich subject?"

    def get_options(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return [(subject.title, {'subject_pk': subject.pk}, \
                'motswadi.application.SubjectProgressMenu') \
                for idx, subject in enumerate(student.get_subjects())] \
                + self.options


class WelcomeMenu(DynamicMenu):
    """
    Initial welcome/geteway landing menu.
    """
    text = 'Welcome to Motswadi. Select a student.'

    def get_options(self):
        students = Student.objects.all()
        return [(student.full_name, {'student_pk': student.pk}, \
                'motswadi.application.StudentMenu') \
                for idx, student in enumerate(students)]


class MotswadiApplicationWorker(DynamicMenuApplicationWorker):
    """
    Main Motswadi application worker responsible for
    menu navigation and info replies.
    """
    initial_menu = WelcomeMenu
