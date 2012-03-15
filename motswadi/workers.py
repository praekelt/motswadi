import redis
import sys

# Initialize Django ENV.
from django.core.management import setup_environ
from motswadi import settings
setup_environ(settings)

from motswadi.models import Student, Teacher
from twisted.internet.defer import inlineCallbacks
from vumi.application import ApplicationWorker, SessionManager


def class_from_str(str):
    return getattr(sys.modules[__name__], str)


class Menu(object):
    def get_text(self):
        return self.text
    
    def get_options(self):
        return self.options

    def get_response(self, choice):
        options = self.response_menu.get_options()

        return self.response_menu.get_text() + '\n' + '\n'.join(
            ['%s. %s' % (idx, opt[0]) for idx, opt in enumerate(options, 1)])

    def __init__(self, session, choice=None):
        self.session = session
        if choice:
            options = self.get_options()
            resolved_choice = options[int(choice) - 1]
            session.update(resolved_choice[1])
            session['class'] = resolved_choice[2]
            self.response_menu = class_from_str(resolved_choice[2])(session)
        else:
            self.response_menu = self


class DynamicMenuApplicationWorker(ApplicationWorker):
    @inlineCallbacks
    def startWorker(self):
        self.redis_config = self.config.get('redis_config', {})
        self.redis_server = redis.Redis(**self.redis_config)
        self.session_manager = SessionManager(
            r_server=self.redis_server,
            prefix="%(worker_name)s:%(transport_name)s" % self.config,
            max_session_length=getattr(self, 'MAX_SESSION_LENGTH', None)
        )
        yield super(DynamicMenuApplicationWorker, self).startWorker()

    @inlineCallbacks
    def stopWorker(self):
        yield self.session_manager.stop()
        yield super(DynamicMenuApplicationWorker, self).stopWorker()

    def consume_user_message(self, message):
        user_id = message.user()
        #self.redis_server.flushall()
        session = self.session_manager.load_session(user_id)
        if not session:
            session = self.session_manager.create_session(user_id)
        if session.has_key('class'):
            menu_class = getattr(sys.modules[__name__], session['class'])
        else:
            menu_class = self.initial_menu
       
        try:
            menu = menu_class(session, message['content'])
            self.session_manager.save_session(user_id, session)
            self.reply_to(message, menu.get_response(message['content']))
        except Exception, e:
            self.reply_to(message, str(e))


class AttendanceMenu(Menu):
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Attendance record for %s:\nAbsent - %s days." % (student.name, student.nonattendance_set.count())

    options = [
        ('Back', {}, 'StudentMenu')
    ]


class SubjectMarksMenu(Menu):
    options = [
        ('Back', {}, 'StudentMenu')
    ]
    
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Subject marks for %s:\n%s" % (student.name, '\n'.join(['%s - %s%%' % (result.subject.title, result.percentage) for result in student.subjectresult_set.all()]))

class TestResultsMenu(Menu):
    options = [
        ('Back', {}, 'StudentMenu')
    ]
    
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Latest tests results for %s:\n%s" % (student.name, '\n'.join(['%s - %s (%s) - %s%%' % (result.test.subject.title, result.test.title, result.test.date, result.percentage) for result in student.testresult_set.all()[:5]]))
    
class DatesMenu(Menu):
    options = [
        ('Back', {}, 'StudentMenu')
    ]
    
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Important dates for %s:\n%s" % (student.name, '\n'.join(['%s - %s' % (event.title, event.date) for event in student.event_set.all()]))


class TeacherInfoMenu(Menu):
    options = [
        ('Back', {}, 'TeacherMenu')
    ]
    
    def get_text(self):
        teacher = Teacher.objects.get(pk=self.session['teacher_pk'])
        return "Information for %s:\nContact Number - %s" % (teacher.name, teacher.contact_number)

    
class TeacherMenu(Menu):
    options = [
        ('Back', {}, 'StudentMenu')
    ]
    
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Teacher information for %s:" % student

    def get_options(self):
        teachers = Student.objects.get(pk=self.session['student_pk']).teacher_set.all()
        return [('%s - %s' % (teacher.subject.title, teacher.name), {'teacher_pk': teacher.pk}, 'TeacherInfoMenu') for idx, teacher in enumerate(teachers)] + self.options


class StudentMenu(Menu):
    def get_text(self):
        student = Student.objects.get(pk=self.session['student_pk'])
        return "Report choices for %s." % student

    options = [
        ('Attendance.', {}, 'AttendanceMenu'),
        ('Subject marks.', {}, 'SubjectMarksMenu'),
        ('Test results.', {}, 'TestResultsMenu'),
        ('Important dates.', {}, 'DatesMenu'),
        ('Teacher information.', {}, 'TeacherMenu'),
        ('Back', {}, 'WelcomeMenu')
    ]


class WelcomeMenu(Menu):
    text = 'Welcome to Motswadi. Select a student.'

    def get_options(self):
        students = Student.objects.all()
        return [(student.name, {'student_pk': student.pk}, 'StudentMenu') for idx, student in enumerate(students)]


class USSDApplicationWorker(DynamicMenuApplicationWorker):
    """
    Main Motswadi application worker responsible for
    menu navigation and info replies.
    """
    initial_menu = WelcomeMenu
