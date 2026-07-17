from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class Student(AbstractUser):
    verif_token = models.CharField(max_length=500, default="", blank=True)
    is_verified = models.BooleanField(default=False)

    scholarship_needed = models.BooleanField(default=False, blank=True)
    application_deadline = models.DateField(default=date(2029, 6, 27), blank=True, null=True)
    essays_count = models.IntegerField(default=1, blank=True)
    max_attendance_cost = models.IntegerField(default=0, blank=True)
    AP_exams = models.BooleanField(default=True, blank=True)
    min_GPA = models.FloatField(default=0.0, blank=True)
    majors = models.JSONField(default=list, blank=True, null=True)
    competencies = models.JSONField(default=list, blank=True, null=True)
