from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Pelcon


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UpLoad(forms.Form):
    file_field = forms.FileField(label="Chon file", widget=forms.ClearableFileInput(attrs={'multiple': True}))


class DownLoadFile(forms.Form):
    pdf = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
