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

    def __init__(self, file, description, user_id=None, batch=True):

        self.submissions = []
        self.description = description
        self.user_id = user_id
        if zipfile.is_zipfile(file):
            if batch:
                self.process_batch_zipfile(file)
            else:
                self.process_zipfile(file)

    def process_batch_zipfile(self, zfile):
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
                    if not file_path.__contains__("__MACOSX") and "text/" in filetype:

                        dirname = os.path.dirname(file_path)
                        user_id = dirname.split("/")[0]
                        if user_id == "":
                            user_id = "None"

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
                            submission.description = self.description
                            submission.user_id = user_id
                            print(submission.user_id)
                            submission.filename = os.path.basename(file_path)
                            file = zip.open(file_path)
                            submission.file_contents = file.read().decode('utf-8', "ignore")
                            # discard the submission if the file contents is zero lenth
                            if len(submission.file_contents) != 0:
                                self.submissions.append(submission)

    def process_zipfile(self, zfile):
        """
        extracts the uploaded zipfile and saves the files to the database for one user_id.
        files are concatenated into one file.
        filters out binary files.
        :param zfile:
        :return: none
        """
        with ZipFile(zfile) as zip:

            file_paths = [file for file in zip.namelist() if not file.endswith("/")]
            submission = Submission()
            submission.file_contents = ""
            submission.filename = os.path.basename(file_paths[0])
            submission.user_id = self.user_id
            print(submission.user_id)
            submission.description = self.description

            for file_path in file_paths:
                    # check if file is text and not binary
                    filetype = mimetypes.guess_type(file_path)[0]
                    # filters out mac generated files which aren't detected by mimetypes
                    if not file_path.__contains__("__MACOSX") and "text/" in filetype:
                        # concatenate files
                        file = zip.open(file_path)
                        file_content = file.read().decode('utf-8', "ignore")
                        # append file to other files already in the submission
                        submission.file_contents += file_content

            # discard the submission if the file contents is zero lenth
            if len(submission.file_contents) != 0:
                    self.submissions.append(submission)

