from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    year = forms.IntegerField(required=False)
    description = forms.CharField(max_length=20)
    param_t = forms.IntegerField(required=False)
    param_n = forms.IntegerField(required=False)
    min_lines_matched = forms.IntegerField(required=False)
    separation_allowance = forms.IntegerField(required=False)
    match_threshold = forms.IntegerField(required=False)


class APIUploadFileForm(forms.Form):
    file = forms.FileField()