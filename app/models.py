from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_id = models.IntegerField
    user_id = models.CharField
    course_id = models.CharField
    assignment_number = models.IntegerField
    file = models.CharField
    fingerprint = models.CharField
    date = models.DateTimeField('date submitted')