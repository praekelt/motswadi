from django.db import models


class Guardian(models.Model):
    name = models.CharField(
        max_length=128
    )
    students = models.ManyToManyField('motswadi.Student')
    number = models.CharField(max_length=16)


class NonAttendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey('motswadi.Student')


class School(models.Model):
    name = models.CharField(
        max_length=128
    )


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


class Test(models.Model):
    title = models.CharField(
        max_length=128
    )
    subject = models.ForeignKey('motswadi.Subject')
    date = models.DateField()


class ResultBase(models.Model):
    class Meta:
        abstract = True


class TestResult(ResultBase):
    test = models.ForeignKey('motswadi.Test')


class SubjectResult(ResultBase):
    subject = models.ForeignKey('motswadi.Subject')
