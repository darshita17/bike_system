from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import password_validation
from . models import Profile


class CustomerRegistrationForm(UserCreationForm):
	username = forms.CharField(max_length=100,label="Username",widget=forms.TextInput(attrs={'class': 'form-control'}))
	phonenumber = PhoneNumberField(widget=forms.TextInput(attrs={'class':'form-control'}),label="Phone number", required=False)
	email = forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2=forms.CharField(label="Password Confirm",widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ["username", "phonenumber", "email","password1",'password2']
	

class LoginForm(AuthenticationForm):
	username = forms.CharField(max_length=100,label="Username",widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ["username","password1"]


class MyPasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(label="Old Password", strip="Flase",widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'current-password','autofocus':True}))
	new_password1 = forms.CharField(label="New Password", strip="Flase",widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'new-password','autofocus':True}),help_text=password_validation.password_validators_help_text_html())
	new_password2 = forms.CharField(label="Confirm New Password", strip="Flase",widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'new-password'} ))


class MyPasswordResetForm(PasswordResetForm):
	email=forms.EmailField(label="Email",max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(label="New Password", strip="Flase",widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'new-password','autofocus':True}),help_text=password_validation.password_validators_help_text_html())
	new_password2 = forms.CharField(label="Confirm New Password", strip="Flase",widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete':'new-password'} ))


class ProfileUpadateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields =['image']

