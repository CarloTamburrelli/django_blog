from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

'''
	class CreateUserForm(UserCreationForm): #così eredito
		class Meta:
			model = User
			fields = ['username', 'email', 'password1', 'password2']

		def __init__(self, *args, **kwargs):
			super(CreateUserForm, self).__init__(*args, **kwargs)
			self.fields['username'].widget.attrs.update({'class': 'form-control mb-4'})
			self.fields['email'].widget.attrs.update({'class': 'form-control mb-4'})
			self.fields['password1'].widget.attrs.update({'class': 'form-control mb-4'})
			self.fields['password2'].widget.attrs.update({'class': 'form-control mb-4'})

'''