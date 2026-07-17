from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)

    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_private = models.BooleanField()
    scholarships = models.BooleanField()
    application_deadline = models.DateField()
    early_action = models.BooleanField()
    early_decision = models.BooleanField()
    essays_count = models.IntegerField()
    competencies = models.JSONField(default=list)
    attendance_cost = models.IntegerField()
    acceptance_rate = models.IntegerField()
    AP_exams = models.BooleanField()
    min_GPA = models.FloatField()
    description = models.CharField(max_length=1000)
    majors = models.JSONField()

    def __str__(self):
        return self.name