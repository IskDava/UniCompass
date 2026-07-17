from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import auth
from .models import Student
import os, random
from dotenv import load_dotenv
from django.contrib import messages
from main.majors import Major

load_dotenv()

# Create your views here.
def test(request):
    return HttpResponse("Success!")

def signin(request):
    return render(request, "signin.html")

def signup(request):
    return render(request, "signup.html")

def verification(request):
    username = request.POST["username"]
    email_to = request.POST["email"]
    password = request.POST["password"]
    rep_password = request.POST["rep_password"]

    if password != rep_password:
        messages.info(request, "Passwords don't match")
        return redirect("signup")
    if Student.objects.filter(username=username).exists():
        messages.info(request, "Username is already taken")
        return redirect("signup")
    if Student.objects.filter(email=email_to).exists():
        messages.info(request, "Email is already taken")
        return redirect("signup")
    if len(password) < 6:
        messages.info(request, "Password is too short")
        return redirect("signup")
    
    new_user = Student(username=username, email=email_to)
    new_user.set_password(password)

    token = default_token_generator.make_token(new_user)
    new_user.verif_token = token

    new_user.save()

    import resend

    resend.api_key = os.environ.get("RESEND_API_KEY")

    link = f"{request.scheme}://{request.get_host()}/account/activate?token={token}"

    print("Sending email...")
    r = resend.Emails.send({
    "from": "noreply@davashton.com",
    "to": email_to,
    "subject": "Verification on UniCompass",
    "html": f"Hi {username}! follow this <a href={link}>link</a> to activate your account"
    })
    print("Completed")

    return render(request, "verif.html")

def activate_account(request):
    token = request.GET.get("token")

    if token is None:
        return HttpResponseBadRequest("no token provided")

    user = list(Student.objects.filter(verif_token=token))

    if not user:
        return HttpResponseNotFound("user with that token is not found")
    
    user = user[0]

    user.is_verified = True

    auth.login(request, user)

    return redirect('/account/preferences')

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.info(request, "Invalid credentials")
        return redirect("signin")
    
    auth.login(request, user)

    return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')

def delete_account(request):
    request.user.delete()
    return redirect('/')

def show_preferences(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    deadline = str(request.user.application_deadline)
    
    return render(request, "preferences.html", {
        "majors": request.user.majors,
        "competencies": request.user.competencies,
        "scholarship": "yes" if request.user.scholarship_needed else "no",
        "deadline": deadline,
        "essays": request.user.essays_count,
        "max_cost": request.user.max_attendance_cost,
        "ap_exams": "yes" if request.user.AP_exams else "no",
        "min_GPA": request.user.min_GPA
    })

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "profile.html")

def show_majors(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "majors.html", {
        "selected": request.user.majors
    })

def select_majors(request):
    selected = request.POST.getlist('majors')

    request.user.majors = selected
    request.user.save()

    return redirect('/account/preferences')

def show_compet(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, "competencies.html", {
        "selected": request.user.competencies
    });  

def select_compets(request):
    selected = request.POST.getlist('competencies')

    request.user.competencies = selected
    request.user.save()

    return redirect('/account/preferences')

def save_preferences(request):
    scholarship = request.POST['scholarship'] == 'yes'
    application_deadline = request.POST['application-deadline']
    essays_count = int(request.POST['essays'])
    max_attendance_cost = int(request.POST['maximum-cost'])
    AP_exams = request.POST['ap-exams'] == 'yes'
    min_GPA = float(request.POST['minimum-gpa'])

    request.user.scholarship_needed = scholarship
    request.user.application_deadline = application_deadline
    request.user.essays_count = essays_count
    request.user.max_attendance_cost = max_attendance_cost
    request.user.AP_exams = AP_exams
    request.user.min_GPA = min_GPA

    request.user.save()

    return redirect('/')