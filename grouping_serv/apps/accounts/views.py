from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import NameForm
from django.http import HttpResponse


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

def submit_relation(request):
    if request.method == 'POST':
        print()
                    # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
        userid = request.user.id
        if request.user.is_authenticated:
            relation = UserProfile.objects.get(user_id=userid)
        else:
            return render(request, "accounts/profile.html")
        try:
            if request.POST["favored"].split(',') != ['']:
                relation.favored = relation.favored + request.POST["favored"].split(',')
            else:
                relation.favored = relation.favored
            if request.POST["disliked"].split(',') != ['']:
                relation.disliked = relation.disliked + request.POST["disliked"].split(',')
            else:
                relation.disliked = relation.disliked
        except:
            pass
        # print(relation.favored, relation.disliked)
        relation.save()

        #favored=request.POST["favored"], disliked=request.POST["disliked"]
        # form = UserProfile(favored=request.POST["favored"], disliked=request.POST["disliked"])
        # print(f'form = {form}')
        # form.save()
        return render(request, "accounts/profile.html")

    else:
        return render(request, "accounts/profile.html")

def remove_relation(request):
    if request.method == 'POST':
        print()
                    # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
        userid = request.user.id
        if request.user.is_authenticated:
            relation = UserProfile.objects.get(user_id=userid)
        else:
            return render(request, "accounts/profile.html")
        try:
            for i in request.POST["favored"].split(','):
                try:
                    relation.favored.remove(i)
                except ValueError:
                    pass
            for i in request.POST["disliked"].split(','):
                try:
                    relation.disliked.remove(i)
                except ValueError:
                    pass


        except Exception as e:
            print(e)
            pass
        relation.save()


        #favored=request.POST["favored"], disliked=request.POST["disliked"]
        # form = UserProfile(favored=request.POST["favored"], disliked=request.POST["disliked"])
        # print(f'form = {form}')
        # form.save()
        return render(request, "accounts/profile.html")

    else:
        return render(request, "accounts/profile.html")
