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
from app.lib import comparator
# Create your views here.


class IndexView(View):
    def get(self, request):
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'index.html',
            RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'form': UploadFileForm()
            })
        )


class UploadFileView(FormView):
    template_name = 'index.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('report')

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'File uploaded!', fail_silently=True)
        filepath1 = os.path.join(settings.MEDIA_ROOT, self.request.FILES['file'].name)
        filepath2 = os.path.join(settings.MEDIA_ROOT, self.request.FILES['file2'].name)
        comparator.compare(filepath1, filepath2)
        return super(UploadFileView, self).form_valid(form)


class ReportView(View):
    def get(self, request):
        return render(
            request,
            'report.html',
            RequestContext(request,
            {
                'title': 'Report Page',
                'year': datetime.now().year
            })
        )


