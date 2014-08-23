from django.db import models
from datetime import datetime
# Create your models here.

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.IntegerField()
    user_id = models.CharField(max_length=20)
    #course_id = models.CharField(max_length=10)
    #assignment_number = models.IntegerField()
    filename = models.TextField()
    file_contents = models.TextField()
    fingerprint = models.TextField(null=True)
    date = models.DateTimeField('date submitted', auto_now_add=True)


class Report (models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.IntegerField()
    match_list = models.TextField()
    date = models.DateTimeField('date submitted', auto_now_add=True)
