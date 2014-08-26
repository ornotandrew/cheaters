from app.models import Submission, Report
from lib.comparator import Comparator
from lib.UploadFileHandler import FileHandler
from lib.fingerprinter import Fingerprinter
from time import time


class SubmissionController:
    # TODO: name files consistently
    def __init__(self, file):
        print("{0:<35}{1}".format("Process", "Time (s)"))
        print("--------------------------------------------")
        t_total = time()

        # unzip the file and create the submission objects
        t = time()
        filehandler = FileHandler(file)
        submission_list = filehandler.submissions
        t = time()-t
        print("{0:<35}{1:.5f}".format("Extracted "+str(len(submission_list))+" files", t))

        # fill out the fingerprints of the submissions
        t = time()
        for submission in submission_list:
            fingerprinter = Fingerprinter(submission.file_contents)
            submission.fingerprint = fingerprinter.fingerprint
        t = time()-t
        print("{0:<35}{1:.5f}".format("Generated fingerprints", t))

        # save the submissions for later use
        t = time()
        self.submission_id = submission_list[0].submission_id
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
        comparator = Comparator(submission_list)
        t = time()-t
        print("{0:<35}{1:.5f}".format("Performed comparison", t))

        # create the report object and save it
        t = time()
        self.report = Report()
        self.report.submission_id = self.submission_id
        self.report.match_list = comparator.report
        self.report.save()
        t = time()-t
        print("{0:<35}{1:.5f}".format("Saved report with ID "+str(self.report.id), t))
        t_total = time()-t_total
        print("{0:<35}{1:.5f}".format("TOTAL", t_total))
