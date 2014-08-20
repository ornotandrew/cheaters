import os
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED
from app.models import Submission
from cheaters import settings

class FileHandler():

    def __init__(self, file):
        self.file = file

        self.submission_id = self.get_submission_id()
        print(self.submission_id)
        self.submissions = []
        if zipfile.is_zipfile(file):
            self.process_zipfile(file)

    def process_zipfile(self, zfile):

        with ZipFile(zfile, "r", compression=ZIP_DEFLATED) as zip:
            directories = [item for item in zip.namelist() if item.endswith('/')]
            print(directories)
            print(zip.namelist())

            file_names = [file for file in zip.namelist() if not file.endswith("/")]
            for file_name in file_names:

                    submission = Submission()
                    submission.submission_id = self.submission_id
                    submission.user_id = os.path.dirname(file_name)
                    file = zip.open(file_name)
                    submission.file = file.read().decode('utf-8', "ignore")

                    submission.save()
                    self.submissions.append(submission)

    def get_submission_id(self):
        """
        :return: The increment of the current highest submission id
        """
        query = Submission.objects.order_by("-submission_id")
        if not query:
            return 0
        else:
            return query[0].submission_id + 1
