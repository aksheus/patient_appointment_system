from django.conf.urls import patterns,url
from appointment import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=patterns('',
	url(r'^$',views.Index.as_view(),name='index'), 
    url(r'.*back/$',views.Index.as_view(),name='index2'),
    url(r'^.*done/$',views.Form_handle.as_view(),name='form_handle'),
    url(r'^done/results/$',views.Results.as_view(),name='results'),
    url(r'^done/results/$',views.Form_handle.as_view(),name='badresult')
)
urlpatterns+=staticfiles_urlpatterns()