from django import forms
from django.forms import ModelForm
from .models import Office

class OfficeForm(ModelForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	pan = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	vat = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	
	class Meta:
		model = Office
		fields = '__all__'


