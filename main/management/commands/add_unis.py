import json
from main.models import University
from django.core.management.base import BaseCommand
from datetime import datetime, date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('unis.json') as f:
            unis = json.load(f)

        today = datetime.now()
        today = date(today.year, today.month, today.day)

        for uni in unis:
            info = unis[uni]

            info["type"] = info["type"] == "private"

            print(uni)

            deadline: str = info["application deadline"]
            month, day = map(int, deadline.split('/'))
            real_deadline = date(today.year, month, day)

            if real_deadline < today:
                real_deadline = date(today.year + 1, month, day)

            print(real_deadline)

            obj = University(
                name = uni,
                country = info["country"],
                city = info["city"],
                state = info["state"],
                is_private = info["type"],
                scholarships = info["scholarships"],
                application_deadline = real_deadline,
                early_action = info["early action"],
                early_decision = info["early decision"],
                essays_count = info["essays count"],
                competencies = info["competencies"],
                attendance_cost = info["attendance cost"],
                acceptance_rate = info["acceptance rate"],
                AP_exams = info["AP exams"],
                min_GPA = info["min GPA"],
                description = info["description"],
                majors = info["majors"]
            )

            obj.save()