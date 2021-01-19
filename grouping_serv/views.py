from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.base import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    template = loader.get_template("index.html")
    return render(request, "index.html")


def about(request):
    template = loader.get_template("about.html")
    return render(request, "about.html")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
