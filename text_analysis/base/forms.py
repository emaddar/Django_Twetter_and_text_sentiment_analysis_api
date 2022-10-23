from django import forms
from django.core import validators

class SignUp(forms.Form):
    user = forms.CharField(label='User Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='PassWord')
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


#https://docs.djangoproject.com/fr/2.2/topics/forms/

class YourTextForm(forms.Form):
    your_text_field = forms.CharField(widget=forms.Textarea, required=True)
