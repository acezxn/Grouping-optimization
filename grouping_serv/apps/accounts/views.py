from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import NameForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import json

from . import combination_group


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
                        return redirect("/accounts/profile/"+q)
                    else:
                        print()
                        # relation = UserProfile.objects.get_or_create(id=request.user.id, defaults={'favored': [''], 'disliked': ['']})
                        userid = request.user.id
                        relation = UserProfile.objects.get(user_id=userid)

                        # post data
                        try:
                            if request.POST["favored"].split(",") != [""]:
                                idx = 0
                                favored = json.loads(relation.favored)
                                print(favored)
                                for data in favored:
                                    print(data)
                                    if data[0] == q:
                                        print(
                                            [data[0], data[1] + request.POST["favored"].split(",")]
                                        )
                                        favored[idx] = [
                                            data[0],
                                            data[1] + request.POST["favored"].split(","),
                                        ]
                                        relation.favored = json.dumps(favored)
                                        break
                                    idx += 1
                            else:
                                pass
                            if request.POST["disliked"].split(",") != [""]:
                                idx = 0
                                disliked = json.loads(relation.disliked)
                                for data in disliked:
                                    print(data)
                                    if data[0] == q:
                                        print(
                                            [data[0], data[1] + request.POST["disliked"].split(",")]
                                        )
                                        disliked[idx] = [
                                            data[0],
                                            data[1] + request.POST["disliked"].split(","),
                                        ]
                                        relation.disliked = json.dumps(disliked)
                                        break
                                    idx += 1
                            else:
                                relation.disliked = relation.disliked
                        except:
                            pass

                        # remove data
                        try:
                            idx = 0
                            favored = json.loads(relation.favored)
                            for data in favored:
                                if data[0] == q:
                                    for element in request.POST["rm_favored"].split(","):
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
                                    for element in request.POST["rm_disliked"].split(","):
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
                if q in relation.classrooms:
                    joined_user.append(u)
                classes.extend(relation.created)
            print(joined_user)

            if q in classes:
                relation = UserProfile.objects.get(user_id=userid)
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
                                "joined_users": joined_user
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
            return render(request, "accounts/danger.html", {"q":q})
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
                    allowed_join = json.loads(profile.allowed_join)
                    temp = allowed_join
                    for c in temp:
                        if q in c:
                            allowed_join.remove(c)
                    profile.allowed_join = json.dumps(allowed_join)
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
        if request.method == 'POST':
            user = User.objects.all()
            if request.POST["user"] != "":
                exist = False
                for u in user:
                    if request.POST["user"] == u.username:
                        exist = True
                        break
                if exist:
                    allowed_join = json.loads(profile.allowed_join)
                    for c in allowed_join:
                        if c[0] == q:
                            print(allowed_join[allowed_join.index(c)][1])
                            if request.POST["user"] in allowed_join[allowed_join.index(c)][1]:
                                return HttpResponse("User already added")
                            else:
                                allowed_join[allowed_join.index(c)][1].append(request.POST["user"])
                                break
                    print(allowed_join)
                    profile.allowed_join = json.dumps(allowed_join)
                else:
                    return HttpResponse("user does not exist")
            if request.POST["rm_user"] != "":
                exist = False
                for u in user:
                    if request.POST["rm_user"] == u.username:
                        exist = True
                        id = u.id
                        break
                if exist:
                    allowed_join = json.loads(profile.allowed_join)
                    for c in allowed_join:
                        if c[0] == q:
                            try:
                                c[1].remove(request.POST["rm_user"])
                                break
                            except:
                                pass
                    # delete classrooms of tgt
                    userprofile = UserProfile.objects.get(user_id=id)
                    classrooms = userprofile.classrooms
                    try:
                        classrooms.remove(q)
                    except:
                        pass
                    userprofile.classrooms = classrooms

                    # delete favor dislike data
                    favored = json.loads(userprofile.favored)
                    for i in favored:
                        if i[0] == q:
                            favored.remove(i)
                            break
                    disliked = json.loads(userprofile.disliked)
                    for i in disliked:
                        if i[0] == q:
                            disliked.remove(i)
                            break
                    userprofile.favored = json.dumps(favored)
                    userprofile.disliked = json.dumps(disliked)
                    userprofile.save()

                    profile.allowed_join = json.dumps(allowed_join)
                else:
                    return HttpResponse("user does not exist")
            profile.save()



        try:
            return render(request, "accounts/edit.html", {"allowed": json.loads(profile.allowed_join)[profile.created.index(q)][1],
        "classid": q})
        except ValueError:
            return redirect("/accounts/profile")

    else:
        return redirect('/')

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
        return render(request, "accounts/signup.html", {"form": form, "url": "signup"})
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


def classrooms(request):
    print('classrooms')
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        relation = UserProfile.objects.get(user_id=request.user.id)
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
                relation.created.append(request.POST["classid"])
                print(relation.allowed_join)
                allowed_join = json.loads(relation.allowed_join)
                allowed_join.append(
                    [request.POST["classid"], request.POST["allowed_join"].split(",")]
                )
                relation.allowed_join = json.dumps(allowed_join)
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
                    allowed_join = json.loads(relation.allowed_join)

                    for c in allowed_join:
                        print(c)
                        if request.user.username in c[1]:
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
                    return HttpResponse("Joining not allowed")
        else:
            return render(request, "accounts/join.html", {})
    else:
        return redirect("/accounts/login")


def leave(request):

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


def compute(request, q):

    if request.method == "POST":
        src = dict(request.POST)['src[]']
        dst = dict(request.POST)['dst[]']
        rule = []
        for i in range(len(dict(request.POST)['src[]'])):
            rule.append((src[i], dst[i]))
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
                return HttpResponse('Not an natural number')
        except:
            return HttpResponse('Not an natural number')
        G, state = combination_group.start_group(size=size, favor_data=favor_data, total=total, rule=rule)
        if state:
            return render(request, "accounts/comb_compute.html", {"GROUP": G})
        else:
            return HttpResponse('Invalid group size')
        try:
            pass
        except:
            return redirect("/accounts/profile")
    return redirect("/accounts/profile")
