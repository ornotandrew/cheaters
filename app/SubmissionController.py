from app.lib.comparator import Comparator


class SubmissionController:
    def __init__(self, filename_a, filename_b):
        comparator = Comparator(filename_a, filename_b)
        self.result = comparator.result