from django.db import models


class Submission(models.Model):
    """
    this model stores the uploaded file contents and its fingerprints along with meta info
    """
    id = models.AutoField(primary_key=True)
    submission_id = models.IntegerField()
    user_id = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    filename = models.TextField()
    file_contents = models.TextField()
    fingerprint = models.TextField(null=True)
    date = models.DateTimeField('date submitted', auto_now_add=True)


class Report (models.Model):
    """
    this model stores the report for a particular submission
    """
    id = models.AutoField(primary_key=True)
    submission_id = models.IntegerField()
    match_list = models.TextField()
    description = models.CharField(max_length=20)
    date = models.DateTimeField('date submitted', auto_now_add=True)
