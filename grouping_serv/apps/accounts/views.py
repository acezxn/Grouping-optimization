from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import NameForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from . import combination_group


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            id = request.user.id
            obj = UserProfile.create(id)
            obj.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    if not request.user.is_authenticated:
        return render(request, "accounts/signup.html", {"form": form})
    else:
        return redirect("/")


def list_user(request):
    if request.user.is_authenticated:
        user = User.objects.all()
        return render(
            request, "accounts/list.html", {"user": user, "prev": "/accounts/profile"}
        )
    else:
        return redirect("/accounts/profile")


def submit_relation(request):
    if request.method == "POST":
        print()
        # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
        userid = request.user.id
        if request.user.is_authenticated:
            relation = UserProfile.objects.get(user_id=userid)
        else:
            return redirect("/accounts/profile")
        try:
            if request.POST["favored"].split(",") != [""]:
                relation.favored = relation.favored + request.POST["favored"].split(",")
            else:
                relation.favored = relation.favored
            if request.POST["disliked"].split(",") != [""]:
                relation.disliked = relation.disliked + request.POST["disliked"].split(
                    ","
                )
            else:
                relation.disliked = relation.disliked
        except:
            pass
        # print(relation.favored, relation.disliked)
        relation.save()

        # favored=request.POST["favored"], disliked=request.POST["disliked"]
        # form = UserProfile(favored=request.POST["favored"], disliked=request.POST["disliked"])
        # print(f'form = {form}')
        # form.save()
        return redirect("/accounts/profile")

    else:
        return redirect("/accounts/profile")


def remove_relation(request):
    if request.method == "POST":
        print()
        # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
        userid = request.user.id
        if request.user.is_authenticated:
            relation = UserProfile.objects.get(user_id=userid)
        else:
            return redirect("/accounts/profile")
        try:
            for i in request.POST["favored"].split(","):
                try:
                    relation.favored.remove(i)
                except ValueError:
                    pass
            for i in request.POST["disliked"].split(","):
                try:
                    relation.disliked.remove(i)
                except ValueError:
                    pass

        except Exception as e:
            print(e)
            pass
        relation.save()

        # favored=request.POST["favored"], disliked=request.POST["disliked"]
        # form = UserProfile(favored=request.POST["favored"], disliked=request.POST["disliked"])
        # print(f'form = {form}')
        # form.save()
        return redirect("/accounts/profile")

    else:
        return redirect("/accounts/profile")


def compute(request):

    if request.method == "POST":
        print("post")
        all = list(User.objects.all())
        total = []
        G = []
        favor_data = dict()
        for u in all:
            if not u.is_superuser:
                total.append(u.username)
                profile = UserProfile.objects.get(user_id=u.id)
            # return redirect("/accounts/profile")
                favor_data[u.username] = [profile.favored, profile.disliked]
        print(type(combination_group.start_group(size=2, favor_data=favor_data, total=total)))
        G = combination_group.start_group(size=2, favor_data=favor_data, total=total)
    return render(request, "accounts/comb_compute.html", {"GROUP": G})


if __name__ == "__main__":
    print(combination_group.start_group(size=2, favor_data=favor_data, total=total))
