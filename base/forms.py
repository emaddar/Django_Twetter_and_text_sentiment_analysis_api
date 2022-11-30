from django import forms
from django.core import validators
from . import models

class SignUp(forms.Form):
    user = forms.CharField(label='User Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='PassWord')
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


#https://docs.djangoproject.com/fr/2.2/topics/forms/

class YourTextForm(forms.Form):
    your_text_field = forms.CharField(widget=forms.Textarea, required=True)




class UploadFileForm(forms.Form):
    file = forms.FileField()


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ('username', 'first_name','password1','password2', 'api_key','email')