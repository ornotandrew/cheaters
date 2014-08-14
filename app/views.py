from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.forms import UploadFileForm
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from cheaters import settings
import os
from app.lib import comparator, preprocessor
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
        submission = form.save(commit=True)

        filepath_1 = os.path.join(settings.MEDIA_ROOT, submission.file.name)
        filepath_2 = os.path.join(settings.MEDIA_ROOT, submission.file2.name)
        result = comparator.compare(preprocessor.normalize(filepath_1), preprocessor.normalize(filepath_2))

        source1 = highlight(filepath_1, [x[0] for x in result[1]])
        source2 = highlight(filepath_2, [x[1] for x in result[1]])
        return render(self.request, 'report.html', {'data': result, 'percent': result[0],
                                                    'file1': source1, 'file2': source2})

        return render(self.request, 'report.html', {'data': comparison})


class ReportView(View):
    def get(self, request):
        return render(
            request,
            'report.html',
            {
                'title': 'Report Page',
                'year': datetime.now().year
            })


def highlight(filepath, line_numbers):
    with open(filepath, "r") as file:
        source = list(file)

    for line_number in line_numbers:
        source[line_number-1] = "<span class=\"highlight\">"+source[line_number-1]+"</span>"

    return "".join(source)
