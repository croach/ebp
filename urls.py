from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/([^\/]+)/([^\/]+)/export/$', 
        'patient_records.views.export_patient_records'),
    url(r'^admin/?(.*)', admin.site.root),
    url(r'', include('ebp.patient_records.urls')),
)

# If debugging is turned on, use Django's built-in static file serving
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
