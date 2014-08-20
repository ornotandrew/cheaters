from app.lib.comparator import Comparator
from app.lib.UploadFileHandler import FileHandler
from app.lib.fingerprinter import Fingerprinter


class SubmissionController:
    # TODO: name files consistently
    def __init__(self, file):
        filehandler = FileHandler(file)
        submission_list = filehandler.submissions

        # fill out the fingerprints in the models
        for submission in submission_list:
            fingerprinter = Fingerprinter(submission.file_contents)
            submission.fingerprint = fingerprinter.fingerprint

        comparator = Comparator(submission_list)
        self.report = comparator.report
