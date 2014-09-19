import cProfile
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
import operator
from datetime import datetime
from app.submissioncontroller import SubmissionController
from app.models import Report, Submission
from app.forms import UploadFileForm
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy, reverse

import os


class UploadFileView(FormView):
    """
    :return: redirects to report_file_list with the report_id as a parameter
    """

    form_class = UploadFileForm

    def form_valid(self, form):

        file = form.cleaned_data["file"]
        del form.cleaned_data["file"]
        description = form.cleaned_data["description"]
        del form.cleaned_data["description"]

        parameters = {}

        for key, value in form.cleaned_data.items():
            if value is not None:
                parameters[key] = value


        sub_controller = SubmissionController(file, description, **parameters)
        #cProfile.runctx("SubmissionController(form.cleaned_data['file'])", locals(), globals(), "temp/profile.prof")

        self.report = sub_controller.report
        response = {"report_id": self.report.id}
        response = json.dumps(response)

        return HttpResponse(response, content_type="application/json")

    def form_invalid(self, form):
        data = json.dumps(form.errors)

        return HttpResponse(data, status=400, content_type='application/json')


class AboutView(View):
    """
    gives a list of the comparisons in the report
    """
    def get(self, request):
        return render(request, "about.html")


class ReportView(View):
    """
    gives a list of the comparisons in the report
    """
    def get(self, request, report_id):
        report = Report.objects.get(id=report_id)
        report.match_list = eval(report.match_list)
        report.match_list.sort(key=operator.itemgetter("percent_match"), reverse=True)
        # get the corresponding user_id and filename for each file id and insert it into the dictionary
        for match in report.match_list:
            submission = Submission.objects.get(id=match["file_2"])
            match["user2"] = submission.user_id
            submission = Submission.objects.get(id=match["file_1"])
            match["user1"] = submission.user_id

        return render(request, "report.html", {"title": "Report File List",
                                                        "report_id": report_id,
                                                        "object_list": report.match_list})


class ComparisonView(View):
    """
    shows the comparison between 2 given files.
    """
    def get(self, request, report_id, file_1_id, file_2_id):
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
        source1 = highlight(file1.file_contents, line_matches, 0)
        source2 = highlight(file2.file_contents, line_matches, 1)

        return render(
            request,
            "comparison.html",
            {
                "title": "Report Page",
                "year": datetime.now().year,
                "percent_match": comparison["percent_match"],
                "file1": source1,
                "file2": source2
            })


class ReportListView(View):
    """
    lists the reports for submissions flagged
    """
    def get(self, request):
        report_list = Report.objects.all().order_by("-date")

        return render(
            request,
            "report_list.html",
            {
                "title": "Report List Page",
                "year": datetime.now().year,
                "report_list": report_list,
            })


def highlight(file, match_ranges, index):
    col = ["#cc3f3f ", "#379fd8", "#87c540", "#be7cd2", "#ff8ecf", "#e5e155"]

    source = file.splitlines()
    for i, match_range in enumerate(match_ranges):
        for match in match_range:
            line = match[index]
            source[line-1] = r'<span style="color:'+col[i % len(col)]+r';">'+source[line-1]+r'</span>'

    return "\n".join(source)
