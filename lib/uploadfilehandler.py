import datetime
import os
import shutil
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED
import io
from app.models import Submission
from cheaters import settings
import mimetypes

class FileHandler():

    def __init__(self, file):

        self.submission_id = self.get_submission_id()
        self.submissions = []
        if zipfile.is_zipfile(file):
            self.process_zipfile(file)

    def process_zipfile(self, zfile):
        """
        extracts the uploaded zipfile and saves the files to the database.
        files for each user_id are concatenated into one file.
        filters out binary files.
        :param zfile:
        :return: none
        """
        with ZipFile(zfile) as zip:
            submission = Submission()
            file_paths = [file for file in zip.namelist() if not file.endswith("/")]
            for file_path in file_paths:
                    # check if file is text and not binary
                    filetype = mimetypes.guess_type(file_path)[0]
                    # filters out mac generated files which aren't detected by mimetypes
                    if not file_path.__contains__("__MACOSX") and filetype == "text/plain":

                        dirname = os.path.dirname(file_path)
                        # gets the first directory of the dirname incase there are subfolders
                        user_id = dirname.split("/")[0]
                        # concatenate files if it is the same user as previous iteration
                        # the file listing is in order of folders so this should always work to find all files for one user_id
                        if submission.user_id == user_id:
                            file = zip.open(file_path)
                            file_content = file.read().decode('utf-8', "ignore")
                            # if previous file was empty it wouldn't have been added to submission list so add it now
                            if len(submission.file_contents) == 0 and len(file_content) != 0:
                                self.submissions.append(submission)
                            # append file to other files already in the submission
                            submission.file_contents += file_content
                        else:
                            # if a different user_id make a new submission
                            submission = Submission()
                            submission.submission_id = self.submission_id
                            submission.user_id = user_id
                            print(submission.user_id)
                            submission.filename = os.path.basename(file_path)
                            file = zip.open(file_path)
                            submission.file_contents = file.read().decode('utf-8', "ignore")
                            # discard the submission if the file contents is zero lenth
                            if len(submission.file_contents) != 0:
                                self.submissions.append(submission)



    def get_submission_id(self):
        """
        :return: The increment of the current highest submission id
        """
        query = Submission.objects.order_by("-submission_id")

        return 0 if not query else query[0].submission_id + 1
