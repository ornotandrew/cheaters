from app.models import Submission, Report
from lib.comparator import Comparator
from lib.uploadfilehandler import FileHandler
from lib.fingerprinter import Fingerprinter
from time import time
import datetime


class SubmissionController:

    def __init__(self, file, description, admin_submission=True, **kwargs):
        print("{0:<35}{1}".format("Process", "Time (s)"))
        print("--------------------------------------------")
        t_total = time()

        # unzip the file and create the submission objects
        t = time()
        filehandler = None
        if admin_submission:
            filehandler = FileHandler(file, description)
        else:
            filehandler = FileHandler(file, description, batch=False)

        submission_list = filehandler.submissions
        t = time()-t
        print("{0:<35}{1:.5f}".format("Extracted "+str(len(submission_list))+" files", t))

        # fill out the fingerprints and submission_id's of the submissions
        t = time()
        self.submission_id = self.get_submission_id() if admin_submission else -1

        for submission in submission_list:
            submission.submission_id = self.submission_id
            fingerprinter = Fingerprinter(submission.file_contents, submission.filename, **kwargs)
            submission.fingerprint = fingerprinter.fingerprint
        t = time()-t
        print("{0:<35}{1:.5f}".format("Generated fingerprints", t))

        # save the submissions for later use
        t = time()

        if admin_submission:
            Submission.objects.bulk_create(submission_list)
            # retrieve same submissions now that the db has given them all primary keys

            submission_list = Submission.objects.filter(submission_id=self.submission_id)

            # eval all the fingerprints from string to list
            for submission in submission_list:
                submission.fingerprint = eval(submission.fingerprint)
        t = time()-t
        print("{0:<35}{1:.5f}".format("Saved submissions with ID "+str(self.submission_id), t))

        # do the comparison and get the report
        t = time()
        comparator = Comparator(submission_list, compare_history=True, **kwargs)
        t = time()-t
        print("{0:<35}{1:.5f}".format("Performed comparison", t))

        # create the report object and save it
        t = time()
        self.report = Report()
        self.report.submission_id = self.submission_id
        self.report.description = description
        self.report.match_list = comparator.report
        if admin_submission:
            self.report.save()
        t = time()-t
        print("{0:<35}{1:.5f}".format("Saved report with ID "+str(self.report.id), t))
        t_total = time()-t_total
        print("{0:<35}{1:.5f}".format("TOTAL", t_total))

    @staticmethod
    def get_submission_id():
        """
        :return: The increment of the current highest submission id
        """
        query = Submission.objects.order_by("-submission_id")

        return 1 if not query else query[0].submission_id + 1