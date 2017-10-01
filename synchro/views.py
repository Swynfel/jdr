from django.shortcuts import render, redirect

from .models import *
from .forms import *


def is_allowed(view):
    def decorated(request,*args, **kwargs):
        if not(request.user.is_authenticated()):
            return redirect("login")
        if not(hasattr(request.user,"profile") and request.user.profile.validated):# and not(request.user.is_staff):
            return redirect("waiting")
        return view(request,*args, **kwargs)
    return decorated


def default(request):
    return render(request, "base.html")

def index(request):
    return render(request, "base.html")

def waiting(request):
    params = {
        "title":"Attente de confirmation",
        "message":
        """Votre profile est en attente de confirmation. Attendez qu'un administrateur le valide.
        (Un certain administrateur est très probablement en train de subir dans son casert)"""
    }
    return render(request, "simple.html", params)

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            password = PasswordResetForm(request.POST)
            password.is_valid()
            opts = {
                'use_https': request.is_secure(),
                'email_template_name': 'registration/password_reset_email.html',
                'token_generator': default_token_generator,
                'request': request,
            }
            password.save(**opts)
            return redirect("signup-mail-sent")
    else:
        form = SignUpForm() 
    return render(request, "registration/signup.html", {"form": form} )

def signupDone(request):
    params = {
        "title":"Compte crée",
        "message":
        """Votre compte viens d'être crée. Un mail de confirmation vous a été envoyé, dans lequel se trouvent les instructions pour définir votre mot de passe.""",
        "form": form
    }
    return render(request, "simple.html", params)

@is_allowed
def activities(request):
    searched = False
    activities = Activity.objects.none()
    if request.method == "POST":
        form = SearchActivity(request.POST)
        if form.is_valid():
            activities = form.filteredActivities()
            searched = True
    else:
        form = SearchActivity()
    if(not(searched)):
        activities=Activity.objects.all()
    return render(request, "activities.html", {"activities":activities,"form":form})

@is_allowed
def myActivities(request,what='all'):
    activities =Activity.objects.none()
    print(what)
    if(what!='player'):
        playerActivities=Activity.objects.filter(organiser=request.user)
        activities = playerActivities
    if(what!='organiser'):
        organiserActivities=Activity.objects.filter(players=request.user)
        activities = organiserActivities
    if(what=='all'):
        activities = (playerActivities | organiserActivities).distinct()
    return render(request, "my_activities.html", {"activities":activities})

@is_allowed
def newActivity(request):
    if request.method == "POST":
        form = EditActivityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if(key):
                pass
            else:
                activity = Activity.objects.create(**form.cleaned_data)
            # redirect, or however you want to get to the main view
            return redirect("activity-edit",key=activity.id)
    else:
        if(key):
            form = EditActivityForm(Activity.objects.get(id=key))
        else:
            form = EditActivityForm()
    params = {
        "title":"Nouveau Scénario",
        "message":"Veuillez entrer un nom pour votre scénario",
        "form": form
    }
    return render(request, "form/simple.html", params)

@is_allowed
def editActivity(request, key=None):
    activity=None
    if(key):
        activity=Activity.objects.get(id=key)
    if request.method == "POST":
        form = EditActivityForm(request.POST,instance=activity)
        if form.is_valid():
            if(key):
                form.save()
            else:
                activity = Activity.objects.create(organiser=request.user,**form.simple_cleaned_data())
                EditActivityForm(request.POST,instance=activity).save()
            return redirect("activity-edit",key=activity.id)
    else:
        form = EditActivityForm(instance=activity)
    params = {
        "title":"Nouveau Scénario",
        "message":"Veuillez entrer un nom pour votre scénario",
        "form": form
    }
    return render(request, "form/simple.html", params)

@is_allowed
def getActivity(request, key=None):
    activity = Activity.objects.get(pk=key)
    return render(request, "activity.html", {"activity":activity})

@is_allowed
def askActivity(request, key, what='nothing'):
    user = request.user
    activity = Activity.objects.get(id=key)
    return getActivity(request, key)