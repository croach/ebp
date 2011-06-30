from django.contrib import admin
from ebp.patient_records.models import RestartReason, PatientRecord

class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'restart_reasons_desc', 'vesicant_irritant',
                    'iv_attempts',)
    search_fields = ('patient_id',)
    filter_horizontal = ('restart_reasons',)
    
admin.site.register(RestartReason)
admin.site.register(PatientRecord, PatientRecordAdmin)
