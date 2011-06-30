from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from ebp.patient_records.models import PatientRecord, RestartReason

class PatientRecordForm(ModelForm):
    patient_id = forms.IntegerField(
        label='Patient ID', 
        widget=forms.TextInput(attrs={'class':'text'}))
        
    vesicant_irritant = forms.BooleanField(
        label='Vesicant/Irritant?',
        widget=forms.CheckboxInput(attrs={'class':'checkbox'}),
        required=False)
    
    iv_attempts = forms.IntegerField(
        label='IV Attempts',
        widget=forms.TextInput(attrs={'class':'text'}),
        required=False)
        
    restart_reasons = forms.ModelMultipleChoiceField(
        label='Restart Reasons',
        widget=forms.SelectMultiple(attrs={'class':'select'}),
        queryset=RestartReason.objects.all(),
        required=False)
        
    def clean(self):
        """
        Overriden clean method makes sure that the iv_attempts value
        defaults to 0 before saving.
        """
        cleaned_data = self.cleaned_data
        iv_attempts = cleaned_data['iv_attempts']
        if not iv_attempts:
            cleaned_data['iv_attempts'] = 0
        return cleaned_data
	
    class Meta:
        model = PatientRecord
    
		
