from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from motswadi.views import CreateAssessmentResultView, RollCallView, \
        UpdateAssessmentResultView


admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^$',
        login_required(TemplateView.as_view(
            template_name="motswadi/home.html")
        ),
        name='home'
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^accounts/',
        include('django.contrib.auth.urls')
    ),
    url(
        r'^create-assessment-result$',
        CreateAssessmentResultView.as_view(),
        name='create_assessment_result'
    ),
    url(
        r'^roll-call$',
        RollCallView.as_view(),
        name='roll_call'
    ),
    url(
        r'^update-assessment-result/(?P<pk>\d+)$',
        UpdateAssessmentResultView.as_view(),
        name='update_assessment_result'
    ),
)
