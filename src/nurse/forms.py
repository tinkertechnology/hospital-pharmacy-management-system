from django import forms
from django.forms import ModelForm
from account.models import Account, Nurse
from department.models import Department


class NurseForm(ModelForm):
	fk_user = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label='--Select Option --', widget=forms.Select(attrs={'class':'form-control'}), required=False)
	fk_department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='--Select Option --', widget=forms.Select(attrs={'class':'form-control'}), required=False)
	
	class Meta:
		model = Nurse
		fields = '__all__'


