from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.SubmissionController import SubmissionController
from app.lib.UploadFileHandler import FileHandler
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
        #submission = form.save(commit=True)
        filehandler = FileHandler(form.cleaned_data['file'])
        submissions = filehandler.submissions

        sub_controller = SubmissionController(submissions)
        #result = sub_controller.result

        #source1 = highlight(filepath_1, [x[0] for x in result[1]])
        #source2 = highlight(filepath_2, [x[1] for x in result[1]])
        #return render(self.request, 'report.html', {'data': result, 'percent': result[0],
         #                                           'file1': source1, 'file2': source2})
        return render(self.request, 'report.html',)





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
