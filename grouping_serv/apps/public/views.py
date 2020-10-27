from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    template = loader.get_template("index.html")
    return render(request, "index.html")


def about(request):
    template = loader.get_template("about.html")
    return render(request, "about.html")
