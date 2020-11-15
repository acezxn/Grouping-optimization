from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    user = User.objects.all()
    n = len(user)
    template = loader.get_template("index.html")
    return render(request, "index.html", {
    "url": "home", "users": n})


def about(request):
    template = loader.get_template("about.html")
    return render(request, "about.html", {
    "url": "about"})
