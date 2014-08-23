from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.SubmissionController import SubmissionController

from app.forms import UploadFileForm
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from cheaters import settings
import os
# Create your views here.


class IndexView(View):
    def get(self, request):
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'index.html',
            {
                'title': 'Home Page',
                'year': datetime.now().year,
                'form': UploadFileForm()
            })


class UploadFileView(FormView):
    template_name = 'index.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('report')

    def form_valid(self, form):
        sub_controller = SubmissionController(form.cleaned_data['file'])
        report = sub_controller.report

        return render(self.request, 'report.html', {'data': "",
                                                    'percent': report[0]["percent_match"],
                                                    })





class ReportView(View):
    def get(self, request):
        return render(
            request,
            'report.html',
            {
                'title': 'Report Page',
                'year': datetime.now().year
            })


def highlight(file_path, line_numbers):
    with open(file_path, "r") as file:
        source = list(file)

    for line_number in line_numbers:
        source[line_number-1] = "<span class=\"highlight\">"+source[line_number-1]+"</span>"

    return "".join(source)
