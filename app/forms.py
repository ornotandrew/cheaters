from django import forms
from django.forms import ModelForm
from app.models import Submission

class UploadFileForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
