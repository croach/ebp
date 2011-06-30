from django.conf.urls.defaults import *

urlpatterns = patterns(
	'ebp.patient_records.views',
	url(r'^summary/$', 'summary', name='summary'),
	url(r'^$', 'index', name='home'),
)
