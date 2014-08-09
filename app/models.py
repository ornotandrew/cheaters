from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_id = models.IntegerField()
    user_id = models.CharField(max_length=20)
    course_id = models.CharField(max_length=10)
    assignment_number = models.IntegerField()
    file = models.TextField()
    fingerprint = models.TextField()
    date = models.DateTimeField('date submitted')