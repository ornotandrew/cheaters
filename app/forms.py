from django import forms
from django.forms import ModelForm
from app.models import Submission

class UploadFileForm(forms.Form):
    file = forms.FileField()
