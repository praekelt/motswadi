from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from motswadi.models import Test, TestResult


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(TemplateView.as_view(template_name="motswadi/home.html")), name='home'),
    url(r'^create/test$', login_required(CreateView.as_view(model=Test)), name='create_test'),
    url(r'^create/test-result$', login_required(CreateView.as_view(model=TestResult)), name='create_test_result'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
