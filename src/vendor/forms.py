from django import forms
from django.forms import ModelForm
from .models import Vendor

class VendorForm(ModelForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	pan = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	mobile = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
	email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	website = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	notes = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = Vendor
		fields = '__all__'


