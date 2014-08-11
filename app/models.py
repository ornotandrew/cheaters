from django.db import models
from datetime import datetime
# Create your models here.

class Submission(models.Model):
    #submission_id = models.IntegerField(default=0)
    #user_id = models.CharField(max_length=20)
    #course_id = models.CharField(max_length=10)
    #assignment_number = models.IntegerField()
    file = models.FileField(upload_to='.')
    #fingerprint = models.TextField()
    #date = models.DateTimeField('date submitted',default=datetime.now())