from django.db import models
from django.contrib.auth.models import User


class Guardian(models.Model):
    name = models.CharField(
        max_length=128
    )
    students = models.ManyToManyField('motswadi.Student')
    contact_number = models.CharField(max_length=16)


class NonAttendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey('motswadi.Student')

    class Meta:
        unique_together = ("date", "student",)

    def __unicode__(self):
        return "%s - %s" % (self.student.name, self.date)


class Teacher(User):
    school = models.ForeignKey('motswadi.School')
    contact_number = models.CharField(max_length=16)

    def __unicode__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.username)


class AssessmentResult(models.Model):
    title = models.CharField(
        max_length=128
    )
    subject = models.ForeignKey('motswadi.Subject')
    student = models.ForeignKey('motswadi.Student')
    percentage = models.IntegerField()

    class Meta:
        unique_together = ("title", "subject", "student",)


class School(models.Model):
    name = models.CharField(
        max_length=128
    )

    def __unicode__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(
        max_length=128
    )
    school = models.ForeignKey('motswadi.School')
    grade = models.IntegerField()
    class_teacher = models.ForeignKey(
        'motswadi.Teacher',
        help_text="Class/guardian teacher."
    )

    def __unicode__(self):
        return "%s, Gr %s (%s %s)" % (self.full_name, self.grade, \
                self.class_teacher.first_name, self.class_teacher.last_name)


class Subject(models.Model):
    title = models.CharField(
        max_length=128
    )

    def __unicode__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(
        max_length=128
    )
    date = models.DateField()
    students = models.ManyToManyField('motswadi.Student')

    def __unicode__(self):
        return "%s - %s" % (self.title, self.date)
