from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect

from datetime import datetime
from app.SubmissionController import SubmissionController
from app.models import Report, Submission
from app.forms import UploadFileForm
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy, reverse

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
    """
    :return: redirects to report_file_list with the report_id as a parameter
    """
    template_name = "index.html"
    form_class = UploadFileForm

    def form_valid(self, form):
        sub_controller = SubmissionController(form.cleaned_data['file'])
        self.report = sub_controller.report

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("report_file_list", kwargs={"report_id": self.report.id})


class ReportFileListView(View):
    """
    gives a list of the comparisons in the report
    """
    def get(self, request, report_id):
        report = Report.objects.get(id=report_id)
        report.match_list = eval(report.match_list)

        return render(request,"report_file_list.html", {"title": "Report File List","report_id": report_id, "object_list": report.match_list})


class ReportView(View):
    """
    shows the comparison between 2 given files.
    """
    def get(self, request,report_id, file_1_id, file_2_id):
        report = Report.objects.get(id=report_id)
        report.match_list = eval(report.match_list)
        file_1_id = int(file_1_id)
        file_2_id = int(file_2_id)
        #need to find the particular comparison comparing the 2 files with file_1_id and file_2_id
        comparison = [x for x in report.match_list if x["file_1"] == file_1_id and x["file_2"] == file_2_id][0]

        line_matches = comparison["line_matches"]
        # get the two sources files from the database
        file1 = Submission.objects.get(id=file_1_id)
        file2 = Submission.objects.get(id=file_2_id)
        # highlight the necessary lines
        source1 = highlight(file1.file_contents, [x[0] for x in line_matches])
        source2 = highlight(file2.file_contents, [x[1] for x in line_matches])

        return render(
            request,
            "report.html",
            {
                "title": "Report Page",
                "year": datetime.now().year,
                "percent_match": comparison["percent_match"],
                "file1": source1,
                "file2": source2
            })


def highlight(file, line_numbers):

    source = file.splitlines()
    for line_number in line_numbers:
        source[line_number-1] = "<span class=\"highlight\">"+source[line_number-1]+"</span>"

    return "\n".join(source)
