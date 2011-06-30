from django.shortcuts import render_to_response
from django.http import HttpResponse
from ebp.patient_records.forms import PatientRecordForm
from ebp.patient_records.models import PatientRecord, RestartReason
from django.utils import simplejson
import csv

def index(request):
	"""
	This is the main page for the EBP application
	"""
	if request.method == 'POST':
	    form = PatientRecordForm(request.POST)
	    if form.is_valid():
	        form.save()
	        status = simplejson.dumps({'status':'success'})
	        return HttpResponse(status, mimetype='application/json')
	form = PatientRecordForm(auto_id='%s')
	return render_to_response('index.html', {'form': form})

def summary(request):
    """
    This function returns a JSON object represent the summary data 
    for all of the patient records in the database
    """
    data = {'Yes':[], 'No':[], 'labels':{}}
    reasons = zip(list(range(RestartReason.objects.count())), 
                  RestartReason.objects.order_by('reason_id'))
    for i, reason in reasons:
        iv_attempts = __iv_attempts(reason.reason_id)
        data['Yes'].append(iv_attempts[True])
        data['No'].append(iv_attempts[False])
        data['labels'][i] = reason.reason_id
    return HttpResponse(simplejson.dumps(data), 
        mimetype='application/javascript')
        
def export_patient_records(request, app, model):
    """
    This view exports all patient records in the database to a csv file.
    """
    restart_reasons = [r.reason_id for r in RestartReason.objects.order_by('reason_id')]
    
    header_row = ['Patient ID', 'Vesicant/Irritant?', 'IV Attempts']
    header_row += restart_reasons
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ebp.csv'    
    writer = csv.writer(response)
    
    # Write the header (i.e., titles) row
    writer.writerow(header_row)
    
    for p in PatientRecord.objects.order_by('patient_id'):
        patient_restart_reasons = [r.reason_id for r in p.restart_reasons.order_by('id')]
        row = [p.patient_id, p.vesicant_irritant, p.iv_attempts]
        row += [r in patient_restart_reasons for r in restart_reasons]
        writer.writerow(row)
    
    return response

def __iv_attempts(reason_id):
    """
    This function takes a reason id and returns the total number of IV
    attempts for that restart reason grouped by the Vesicant/Irritant?
    field.
    """
    qs = PatientRecord.objects.filter(
        restart_reasons__reason_id__contains=reason_id).extra(
            {'sum':'sum(iv_attempts)'}).values('vesicant_irritant', 'sum')
    qs.query.group_by = ['vesicant_irritant']

    totals = list(qs)
    if len(totals) == 1: 
        return {totals[0]['vesicant_irritant']:totals[0]['sum'],
            not totals[0]['vesicant_irritant']:0}
    elif len(totals) == 2: 
        return {totals[0]['vesicant_irritant']:totals[0]['sum'], 
            totals[1]['vesicant_irritant']:totals[1]['sum']}
    else: 
        return {False: 0, True: 0}
