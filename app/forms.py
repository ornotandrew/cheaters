from django import forms
from django.forms import ModelForm
from app.models import Submission

class UploadFileForm(forms.Form):
    file = forms.FileField()
    year = forms.IntegerField()
    description = forms.CharField(max_length=20)
    param_t = forms.IntegerField(required=False)
    param_n = forms.IntegerField(required=False)