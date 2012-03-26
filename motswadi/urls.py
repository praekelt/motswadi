from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from motswadi.views import CreateAssessmentResultView, CreateEventView,\
        RollCallView, UpdateAssessmentResultView, \
        UpdateAssessmentResultsView, UpdateEventView, UpdateEventsView


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
        r'^create-event$',
        CreateEventView.as_view(),
        name='create_event'
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
    url(
        r'^update-assessment-results$',
        UpdateAssessmentResultsView.as_view(),
        name='update_assessment_results'
    ),
    url(
        r'^update-event/(?P<pk>\d+)$',
        UpdateEventView.as_view(),
        name='update_event'
    ),
    url(
        r'^update-events$',
        UpdateEventsView.as_view(),
        name='update_events'
    ),
)
