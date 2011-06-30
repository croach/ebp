from django.db import models

class RestartReason(models.Model):
    reason_id = models.CharField(max_length=1, unique=True)
    description = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s - %s" % (self.reason_id, self.description)

    class Meta:
        ordering = ('reason_id',)

class PatientRecord(models.Model):
    patient_id = models.IntegerField(verbose_name='Patient ID')
    iv_attempts = models.IntegerField(default=0,
        verbose_name='IV Attempts')
    vesicant_irritant = models.BooleanField(default=False, 
        verbose_name='Vesicant/Irritant?')
    restart_reasons = models.ManyToManyField(RestartReason, 
        verbose_name='Restart Reasons', null=True, blank=True)

    def restart_reasons_desc(self):
        return ', '.join([r.reason_id for r in self.restart_reasons.all()])
    restart_reasons_desc.short_description = 'Restart Reasons'

    def __unicode__(self):
        return "%d | %s | %s | %d" % (self.patient_id, 
                                      self.restart_reasons_desc(),
                                      self.vesicant_irritant,
                                      self.iv_attempts)

    class Meta:
        ordering = ('patient_id',)
