from django.shortcuts import render, redirect
from .models import University
from django.http import JsonResponse

# Create your views here.
def home(request):
    user = request.user

    if user.is_authenticated:
        return render(request, "home.html", {"username": user.username})
    else:
        return render(request, "guest.html")
    

def show_fyp(request):
    compets = request.user.competencies
    compets = set(map(str.lower, compets))

    unis = {}
    for uni in University.objects.all():
        common = compets & set(uni.competencies)
        unis[uni] = len(common)

    recs = sorted(unis.keys(), key=lambda k: -unis[k])
    
    res = []
    for rec in recs:
        if unis[rec] > 0:
            res.append(rec)

    return render(request, "fyp.html", {
        "unis": res
    })

def show_search(request):
    if not request.user.is_authenticated:
        return redirect('/')

    return render(request, "explore.html")

def get_uni(request, id):
    uni = University.objects.filter(id=id)[0]

    return render(request, "unicard.html", {
        "uni": uni, "user": request.user
    })

def search(request):
    prompt: str = request.POST['prompt']

    res = []
    for uni in University.objects.all():
        if prompt.lower() in uni.name.lower():
            res.append(uni)

    return render(request, "search_res.html", {
        "res": res
    })