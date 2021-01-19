from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

def index(request):
    normal_users = 0
    user = User.objects.all()
    for u in user:
        if not u.is_superuser:
            normal_users += 1
    template = loader.get_template("index.html")
    return render(request, "index.html", {
    "url": "home", "users": normal_users})


def about(request):
    template = loader.get_template("about.html")
    return render(request, "about.html", {
    "url": "about"})

# def test(request):
#     output = _('hello')
#     return HttpResponse(output)
