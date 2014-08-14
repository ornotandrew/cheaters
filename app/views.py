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
                'title':'Home Page',
                'year':datetime.now().year,
                'form': UploadFileForm()
            })



class UploadFileView(FormView):
    template_name = 'index.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('report')

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'File uploaded!', fail_silently=True)

        filepath1 = os.path.join(settings.MEDIA_ROOT, self.request.FILES['file'].name)
        filepath2 = os.path.join(settings.MEDIA_ROOT, self.request.FILES['file2'].name)

        comparison = comparator.compare(preprocessor.normalize(filepath1), preprocessor.normalize(filepath2))

        print(comparison)
        source1 = highlight(filepath1, comparison[1][0])
        source2 = highlight(filepath2, comparison[1][1])
        return render(self.request, 'report.html', {'data': comparison, 'percent': comparison[0], 'file1': source1, 'file2': source2})


        return render(self.request,'report.html',{'data' : comparison})



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
    print(len(source))
    print(line_numbers[-1])
    for i in line_numbers:
        if not i >= len(source):
            source[i] = "<span class=\"highlight\">"+source[i]+"</span>"

    return "".join(source)
