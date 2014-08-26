from app.models import Submission, Report
from lib.comparator import Comparator
from lib.UploadFileHandler import FileHandler
from lib.fingerprinter import Fingerprinter


class SubmissionController:
    # TODO: name files consistently
    def __init__(self, file):
        # unzip the file and create the submission objects
        filehandler = FileHandler(file)
        submission_list = filehandler.submissions
        print(" ~ Extracted {0} files".format(len(submission_list)))

        # fill out the fingerprints of the submissions
        for submission in submission_list:
            fingerprinter = Fingerprinter(submission.file_contents)
            submission.fingerprint = fingerprinter.fingerprint
        print(" ~ Generated fingerprints")

        # save the submissions for later use
        # TODO: some kind of bulk add?

        self.submission_id = submission_list[0].submission_id
        # save all submissions in a single query
        Submission.objects.bulk_create(submission_list)
        # retrieve same submissions now that the db has given them all primary keys
        submission_list = Submission.objects.filter(submission_id = self.submission_id)
        # eval all the fingerprints from string to list
        for submission in submission_list:
            submission.fingerprint = eval(submission.fingerprint)

        print(" ~ Saved submissions with ID {0}".format(self.submission_id))

        # do the comparison and get the report
        comparator = Comparator(submission_list)

        # create the report object and save it
        self.report = Report()
        self.report.submission_id = self.submission_id
        self.report.match_list = comparator.report
        self.report.save()
        print(" ~ Saved report with ID {0}".format(self.report.id))
