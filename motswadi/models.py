from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class AssessmentResult(models.Model):
    title = models.CharField(
        max_length=128
    )
    subject = models.ForeignKey('motswadi.Subject')
    student = models.ForeignKey('motswadi.Student')
    percentage = models.IntegerField()

    class Meta:
        ordering = ('subject__title', 'title', 'student__full_name',)
        unique_together = ("title", "subject", "student",)

    def __unicode__(self):
        return "%s: %s - %s" % (self.subject.title, self.title, \
                self.student.full_name)

    def get_absolute_url(self):
        return reverse("update_assessment_result", kwargs={'pk': self.pk})


class Event(models.Model):
    title = models.CharField(
        max_length=128
    )
    date = models.DateField()
    time = models.TimeField()
    students = models.ManyToManyField('motswadi.Student')
    school = models.ForeignKey('motswadi.School')

    class Meta:
        ordering = ('date', 'time', 'title',)
        unique_together = ("title", "school",)

    def __unicode__(self):
        return "%s %s - %s" % (self.date, self.time, self.title)

    def get_absolute_url(self):
        return reverse("update_event", kwargs={'pk': self.pk})


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

    class Meta:
        ordering = ('grade', 'full_name', )

    def __unicode__(self):
        return "%s (Gr%s)" % (self.full_name, self.grade)

    def get_subjects(self):
        results = AssessmentResult.objects.filter(student=self)
        return list(set([result.subject for result in results]))


class Subject(models.Model):
    title = models.CharField(
        max_length=128
    )

    def __unicode__(self):
        return self.title


class Teacher(User):
    school = models.ForeignKey('motswadi.School')
    contact_number = models.CharField(max_length=16)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
