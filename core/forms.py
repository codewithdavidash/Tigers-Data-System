from django.contrib.auth.forms import (
  AuthenticationForm,
  UserCreationForm,
)
from django import forms
from .models import *


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'doc_type', 'description', 'file']


class LoginForm(AuthenticationForm):
  pass


class RegisterForm(UserCreationForm):
  pass