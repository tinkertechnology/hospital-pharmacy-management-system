from django import forms
from django.forms import ModelForm
from .models import Vendor

class VendorForm(ModelForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	pan = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	
	class Meta:
		model = Vendor
		fields = '__all__'


