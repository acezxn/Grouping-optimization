from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import NameForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


import json
import random
import string

from . import combination_group


def check_exist(word):
    users = User.objects.all()
    for user in users:
        if word == user.username:
            return 1
    return 0


def normalize(words):

    for word in words:
        if word == '':
            continue
        stat = check_exist(word)
        print(words, stat)
        if stat == 0:
            return words, 0
    return words, 1
    # try:
    #     new_words = []
    #     for word in words:
    #         new_words.append(word.replace(" ", ""))
    #     for word in new_words:
    #         for c in word:
    #             if c not in (string.ascii_letters + string.digits):
    #                 return words, 0
    #     return new_words, 1
    # except:
    #     return words, 0


def ProfileView(request, q):

    if request.user.is_authenticated:
        if request.method == "POST":
            userid = request.user.id
            user = User.objects.all()
            classes = []
            for u in user:
                relation = UserProfile.objects.get(user_id=u.id)
                classes.extend(relation.created)

            if q in classes:
                relation = UserProfile.objects.get(user_id=userid)
                if q in relation.classrooms:
                    if q in relation.created:
                        return redirect("/accounts/profile/" + q)
                    else:
                        print()
                        # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
                        userid = request.user.id
                        relation = UserProfile.objects.get(user_id=userid)

                        # post data
                        try:
                            processed_data, state = normalize(
                                request.POST["favored"].split(","))
                            print('processed_data: ', processed_data)
                            if state == 1:
                                if processed_data != [""]:
                                    idx = 0
                                    favored = json.loads(relation.favored)
                                    print(favored)
                                    for data in favored:
                                        print(data)
                                        if data[0] == q:
                                            print(
                                                [data[0], data[1] + processed_data]
                                            )
                                            favored[idx] = [
                                                data[0],
                                                data[1] + processed_data,
                                            ]
                                            relation.favored = json.dumps(
                                                favored)
                                            break
                                        idx += 1
                            else:
                                return HttpResponse('Cannot find specified user')
                            # if request.POST["favored"].replace(" ", "").split(",") != [""]:
                            #
                            # else:
                            #     pass
                            processed_data, state = normalize(
                                request.POST["disliked"].split(","))
                            if state == 1:
                                if processed_data != [""]:
                                    idx = 0
                                    disliked = json.loads(relation.disliked)
                                    for data in disliked:
                                        print(data)
                                        if data[0] == q:
                                            print(
                                                [data[0], data[1] + processed_data]
                                            )
                                            disliked[idx] = [
                                                data[0],
                                                data[1] + processed_data,
                                            ]
                                            relation.disliked = json.dumps(
                                                disliked)
                                            break
                                        idx += 1
                            else:
                                return HttpResponse('Cannot find specified user')
                            # if request.POST["disliked"].replace(" ", "").split(",") != [""]:
                            #
                            # else:
                            #     relation.disliked = relation.disliked
                        except:
                            pass

                        # remove data
                        try:
                            idx = 0
                            favored = json.loads(relation.favored)
                            for data in favored:
                                if data[0] == q:
                                    for element in request.POST["rm_favored"].replace(" ", "").split(","):
                                        data[1].remove(element)

                                    favored[idx] = [data[0], data[1]]
                                    relation.favored = json.dumps(favored)
                                    break
                                idx += 1

                        except Exception as e:
                            print(e)
                            pass
                        try:
                            idx = 0
                            disliked = json.loads(relation.disliked)
                            for data in disliked:
                                if data[0] == q:
                                    for element in request.POST["rm_disliked"].replace(" ", "").split(","):
                                        data[1].remove(element)

                                    disliked[idx] = [data[0], data[1]]
                                    relation.disliked = json.dumps(disliked)
                                    break
                        except Exception as e:
                            print(e)
                            pass
                            idx += 1

                        # print(relation.favored, relation.disliked)
                        relation.save()

                        return redirect("/accounts/profile/" + q)
        #
        else:
            # GET request
            print(q)
            userid = request.user.id
            user = User.objects.all()
            classes = []
            joined_user = []
            for u in user:
                relation = UserProfile.objects.get(user_id=u.id)
                if (q in relation.classrooms) and (q not in relation.created):
                    joined_user.append(u)
                classes.extend(relation.created)
            print(joined_user)

            if q in classes:
                relation = UserProfile.objects.get(user_id=userid)
                codes = json.loads(relation.passcode)
                code = ""
                for c in codes:
                    if c[0] == q:
                        code = c[1]
                if q in relation.classrooms:
                    if q in relation.created:

                        return render(
                            request,
                            "accounts/profile.html",
                            {
                                "user": request.user,
                                "classid": q,
                                "favored": json.loads(relation.favored),
                                "disliked": json.loads(relation.disliked),
                                "created": 1,
                                "url": "accounts",
                                "joined_users": joined_user,
                                "passcode": code
                            },
                        )
                    else:
                        return render(
                            request,
                            "accounts/profile.html",
                            {
                                "user": request.user,
                                "classid": q,
                                "favored": json.loads(relation.favored),
                                "disliked": json.loads(relation.disliked),
                                "created": 0,
                                "url": "accounts"
                            },
                        )
                else:
                    return HttpResponse("Classroom not yours")
            else:
                return HttpResponse("No such classroom")

        #     return redirect("/accounts/profile")
        # print(json.loads(request.user.profile.favored))

    else:
        return redirect("/accounts/login")


def dangerzone(request, q):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=request.user.id)
        if q in profile.created:
            return render(request, "accounts/danger.html", {"q": q})
        else:
            return redirect("/accounts/profile")
    else:
        return redirect("/accounts/login")


def remove(request, q):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile = UserProfile.objects.get(user_id=request.user.id)
            if request.POST['verify'] == request.user.username:
                if q in profile.created:
                    created = profile.created
                    classrooms = profile.classrooms
                    created.remove(q)
                    classrooms.remove(q)
                    profile.created = created
                    profile.classrooms = classrooms

                    print(profile.created)
                    passcode = json.loads(profile.passcode)
                    temp = passcode
                    for c in temp:
                        if q in c:
                            passcode.remove(c)
                    profile.passcode = json.dumps(passcode)
                    profile.save()
                    users = User.objects.all()
                    for u in users:
                        userprofile = UserProfile.objects.get(user_id=u.id)
                        favored = json.loads(userprofile.favored)
                        temp = favored
                        for i in temp:
                            if q in i:
                                favored.remove(i)

                        disliked = json.loads(userprofile.disliked)
                        temp = disliked
                        for i in temp:
                            if q in i:
                                disliked.remove(i)
                        try:
                            userprofile.classrooms.remove(q)
                        except:
                            pass
                        userprofile.favored = json.dumps(favored)
                        userprofile.disliked = json.dumps(disliked)
                        userprofile.save()
                    return redirect("/accounts/profile")
                else:
                    return redirect("/accounts/profile")
            else:
                return render(request, "accounts/danger.html", {"error": "incorrect username", "q": q})
        else:
            return redirect("/accounts/profile")
    else:
        return redirect("/accounts/login")


def edit(request, q):

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=request.user.id)
        created = profile.created
        user = User.objects.all()
        joined_user = []
        for u in user:
            relation = UserProfile.objects.get(user_id=u.id)
            if (q in relation.classrooms) and (q not in relation.created):
                joined_user.append(u)
        print(joined_user)
        if q in created:
            if request.method == 'POST':
                pass
            try:
                return render(request, "accounts/edit.html", {"classid": q, "joined_user": joined_user})
            except ValueError:
                return redirect("/accounts/profile")
        else:
            return redirect('/')

    else:
        return redirect('/accounts/login')


def unsign(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['verify'] == request.user.username:
                id = request.user.id
                # obj = UserProfile.delete_user(id)
                profile = UserProfile.objects.filter(user_id=id)
                profile.delete()
                user = User.objects.filter(id=id)
                user.delete()
                # profile.save()
                return redirect("/")
            else:
                return HttpResponse('verification failed')
        else:
            return render(request, "accounts/signout.html")
    else:
        return redirect('/accounts/login')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            to_email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            id = request.user.id
            obj = UserProfile.create(id)
            obj.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    if not request.user.is_authenticated:
        return render(request, "accounts/signup.html", {"form": form, "url": "signup"})
    else:
        return redirect("/")


def list_user(request, q):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=request.user.id)
        if q in profile.classrooms:

            user = User.objects.all()
            classmate = []
            for u in user:
                profile = UserProfile.objects.get(user_id=u.id)
                if q in profile.classrooms:
                    if q not in profile.created:
                        classmate.append(u)
            try:
                classmate.remove(request.user)
            except:
                pass
            return render(
                request, "accounts/list.html", {"users": classmate,
                                                "prev": "/accounts/profile/" + q, "url": "accounts","user": request.user}
            )
        else:
            return redirect("/accounts/profile")
    else:
        return redirect("/accounts/login")


def kick(request, q):
    if request.method == 'POST':
        request.POST['member2kick']
        userlist = User.objects.all()
        for i in userlist:
            if i.username == request.POST['member2kick']:
                id = i.id
                break

        profile = UserProfile.objects.get(user_id=id)
        classrooms = profile.classrooms
        classrooms.remove(q)
        favored = json.loads(profile.favored)
        for e in favored:
            if e[0] == q:
                favored.remove(e)
                break
        disliked = json.loads(profile.disliked)
        for e in disliked:
            if e[0] == q:
                disliked.remove(e)
                break
        profile.favored = json.dumps(favored)
        profile.disliked = json.dumps(disliked)
        profile.classrooms = classrooms
        profile.save()
        try:
            pass
        except Exception as e:
            pass
        return redirect("/accounts/profile")
    else:
        return redirect("/accounts/profile")


def classrooms(request):
    print('classrooms')
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        relation = UserProfile.objects.get(user_id=request.user.id)
        print(relation.classrooms)
        # try:
        #     relation.created.remove('\u200b\n')
        #     relation.classrooms.remove('\u200b\n')
        # except:
        #     pass
        relation.save()
        return render(
            request,
            "accounts/classrooms.html",
            {
                "classrooms": relation.classrooms,
                "created": relation.created,
                "prev": "/",
                "USER": request.user,
                "url": "accounts"
            },
        )
    else:
        return redirect("/accounts/login")


def generate(length):
    numbers = '1234567890'
    code = []
    for i in range(length):
        code.append(random.choice(list(numbers)))
    return ''.join(code)


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.all()
            classes = []
            relation = UserProfile.objects.get(user_id=request.user.id)
            if len(relation.created) >= 5:
                return HttpResponse("Max number of class created reached")
            for u in user:
                userprofile = UserProfile.objects.get(user_id=u.id)
                classes.extend(userprofile.created)

            if request.POST["classid"] in classes:
                return HttpResponse("class already created")
            else:
                for e in list(request.POST["classid"]):
                    valid_char = string.ascii_letters + string.digits
                    if e not in valid_char:
                        return HttpResponse("Invalid class name")
                relation.created.append(request.POST["classid"])
                passcode = json.loads(relation.passcode)

                passcode.append(
                    [request.POST["classid"], generate(8)]
                )
                relation.passcode = json.dumps(passcode)
                relation.classrooms.append(request.POST["classid"])
                relation.save()
                return redirect("/accounts/profile")
        else:
            return render(request, "accounts/create.html", {})
    else:
        return redirect("/accounts/login")


def join(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # print(request.POST["rm_classid"])
            if len(request.POST["rm_classid"]) > 0:
                return leave(request)
            else:
                user = User.objects.all()
                classes = []
                permitted = False
                for u in user:
                    relation = UserProfile.objects.get(user_id=u.id)
                    classes.extend(relation.created)

                for u in user:
                    relation = UserProfile.objects.get(user_id=u.id)
                    passcode = json.loads(relation.passcode)

                    for c in passcode:
                        print(c)
                        if request.POST["passcode"] == c[1]:
                            permitted = True
                            break

                relation = UserProfile.objects.get(user_id=request.user.id)
                if permitted:
                    if request.POST["classid"] in classes:
                        if request.POST["classid"] in relation.classrooms:
                            return HttpResponse("Class already joined")
                        else:
                            relation.classrooms.append(request.POST["classid"])
                            favored = json.loads(relation.favored)
                            disliked = json.loads(relation.disliked)
                            favored.append([request.POST["classid"], []])
                            disliked.append([request.POST["classid"], []])
                            relation.favored = json.dumps(favored)
                            relation.disliked = json.dumps(disliked)
                            relation.save()
                            return redirect("/accounts/profile")
                    else:
                        return HttpResponse("class not exist")
                else:
                    return HttpResponse("Invalid classid or password")
        else:
            return render(request, "accounts/join.html", {})
    else:
        return redirect("/accounts/login")


def leave(request):
    # authentication gate needed
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=request.user.id)
        print(request.POST["rm_classid"] in profile.classrooms)
        if request.POST["rm_classid"] in profile.classrooms:
            if request.POST["rm_classid"] not in profile.created:
                profile.classrooms.remove(request.POST["rm_classid"])
                favored = json.loads(profile.favored)
                try:
                    for f in favored:
                        if f[0] == request.POST["rm_classid"]:
                            favored.remove(f)
                            break
                    profile.favored = json.dumps(favored)
                    disliked = json.loads(profile.disliked)
                    for d in disliked:
                        if d[0] == request.POST["rm_classid"]:
                            disliked.remove(d)
                            break
                except:
                    pass
            else:
                return HttpResponse("You own this classroom")
            profile.disliked = json.dumps(disliked)
            profile.save()
            print("saved")
            return redirect("/accounts/profile")
        else:
            print("invalid")
            return HttpResponse("Invalid selection")
    else:
        return redirect('/accounts/login')


def compute(request, q):
    # authentication gate needed
    if request.user.is_authenticated:
        if request.method == "POST":
            profile = UserProfile.objects.get(user_id=request.user.id)
            if q not in profile.created:
                return redirect("/accounts/profile")
            else:

                src = dict(request.POST)['src[]']
                dst = dict(request.POST)['dst[]']
                rule = []
                for i in range(len(dict(request.POST)['src[]'])):
                    rule.append([src[i], dst[i]])
                print("post")
                all = list(User.objects.all())
                total = []
                G = []
                favor_data = dict()

                for u in all:
                    if u.username != request.user.username:
                        if not u.is_superuser:
                            profile = UserProfile.objects.get(user_id=u.id)
                            if q in profile.classrooms:
                                total.append(u.username)
                                classes = profile.classrooms
                                favored = []
                                disliked = []
                                for f in json.loads(profile.favored):
                                    if f[0] == q:
                                        favored = f[1]
                                for d in json.loads(profile.disliked):
                                    if d[0] == q:
                                        disliked = d[1]
                                favor_data[u.username] = [favored, disliked]
                print(favor_data)
                try:
                    size = int(request.POST['size'])
                    if size <= 0:
                        return HttpResponse('Group size not a natural number')
                except:
                    return HttpResponse('Group size not a natural number')
                G, state = combination_group.start_group(
                    size=size, favor_data=favor_data, total=total, rule=rule)
                if state:
                    return render(request, "accounts/comb_compute.html", {"GROUP": G, "url": "accounts"})
                else:
                    return HttpResponse('Invalid group size')
                try:
                    pass
                except:
                    return redirect("/accounts/profile")

        return redirect("/accounts/profile")
    else:
        return redirect('/accounts/login')

def setting(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect("/accounts/login")
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            return render(request, 'accounts/setting.html', {})
    else:
        return redirect("/accounts/login")
