from django.db import models


class Guardian(models.Model):
    name = models.CharField(
        max_length=128
    )
    students = models.ManyToManyField('motswadi.Student')
    contact_number = models.CharField(max_length=16)


class NonAttendance(models.Model):
    # TODO: Make date and student unique.
    date = models.DateField()
    student = models.ForeignKey('motswadi.Student')

    def __unicode__(self):
        return "%s - %s" % (self.student.name, self.date)


class School(models.Model):
    name = models.CharField(
        max_length=128
    )

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(
        max_length=128
    )
    students = models.ManyToManyField('motswadi.Student')
    subject = models.ForeignKey('motswadi.Subject')
    contact_number = models.CharField(max_length=16)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.subject.title)


class Student(models.Model):
    name = models.CharField(
        max_length=128
    )
    school = models.ForeignKey('motswadi.School')

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(
        max_length=128
    )

    def __unicode__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(
        max_length=128
    )
    subject = models.ForeignKey('motswadi.Subject')
    date = models.DateField()

    def __unicode__(self):
        return "%s - %s - %s" % (self.subject.title, self.date, self.title)


class ResultBase(models.Model):
    student = models.ForeignKey('motswadi.Student')
    percentage = models.IntegerField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s - %s%%" % (self.student.name, self.percentage)


class TestResult(ResultBase):
    test = models.ForeignKey('motswadi.Test')

    class Meta:
        ordering = ['-test__date', ]


class SubjectResult(ResultBase):
    subject = models.ForeignKey('motswadi.Subject')

    def __unicode__(self):
        return "%s - %s - %s%%" % (self.student.name, self.subject.title, \
                self.percentage)


class Event(models.Model):
    title = models.CharField(
        max_length=128
    )
    date = models.DateField()
    students = models.ManyToManyField('motswadi.Student')

    def __unicode__(self):
        return "%s - %s" % (self.title, self.date)
