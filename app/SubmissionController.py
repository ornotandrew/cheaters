from app.lib.comparator import Comparator
from app.lib.UploadFileHandler import FileHandler

class SubmissionController:
    def __init__(self, file):
        filehandler = FileHandler(file)
        submissions = filehandler.submissions
        #comparator = Comparator(filename_a, filename_b)
        #self.result = comparator.result
