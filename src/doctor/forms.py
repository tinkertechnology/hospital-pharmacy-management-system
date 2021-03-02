from django import forms
from django.forms import ModelForm
from account.models import Account, Doctor
from department.models import Department
from specializationtype.models import SpecializationType

class DoctorForm(ModelForm):
	fk_user = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label='--Select Option --', widget=forms.Select(attrs={'class':'form-control'}), required=False)
	fk_department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='--Select Option --', widget=forms.Select(attrs={'class':'form-control'}), required=False)
	fk_specialization_type = forms.ModelChoiceField(queryset=SpecializationType.objects.all(), empty_label='--Select Option --', widget=forms.Select(attrs={'class':'form-control'}), required=False)

	class Meta:
		model = Doctor
		fields = '__all__'


