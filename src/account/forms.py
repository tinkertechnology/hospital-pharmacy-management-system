from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    # mobile = forms.CharField(max_length=254, help_text='Required. Add a valid phone address.')
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid phone address.')

    class Meta:
        model = Account
        fields = ('email','mobile', 'username', 'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password', 'mobile')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			mobile = self.cleaned_data['mobile']
			if not authenticate(mobile=mobile, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email','username', 'mobile' )

	def clean_mobile(self):
		email = self.cleaned_data['mobile']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(mobile=mobile)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(mobile=mobile)
		except Account.DoesNotExist:
			return mobile
		raise forms.ValidationError('Mobile "%s" is already in use.' % account)













