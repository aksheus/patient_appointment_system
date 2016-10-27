from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^nameofsite/',include('appointment.urls',namespace="appointment")),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns+=staticfiles_urlpatterns()