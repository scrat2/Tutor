import datetime
import json
from time import strftime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from lesson.forms import ConnexionForm, ProfileForm, LessonForm, SearchForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lesson.models import Profiles, Lessons, Groups


# Create your views here.
def connexion(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        # Get the form from forms.py and add it to the context to send it to the template.
        form = ConnexionForm()
        context = {
            'form': form
        }
        if request.method == 'POST':
            # Get data from the form
            form = ConnexionForm(request.POST)

            # Clean data to avoid injection
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Check if IDs are good
                user = authenticate(username=username, password=password)
                if user is not None:
                    # If good log user and check the profil create it if needed
                    profile = Profiles.objects.filter(user=user)
                    if not profile.exists():
                        profile = Profiles(user=user)
                        profile.save()
                    login(request, user)
                    return redirect('/home')
                else:
                    context['log'] = False

        return render(request, 'connexion.html', context)


def profil(request):
    if request.user.is_authenticated:

        # Get the form from forms.py and add it to the context to send it to the template.
        form = ProfileForm()
        context = {
            'form': form
        }

        # Get the current user and the corresponding profile
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        context['nbr_heure'] = profile.nbr_heure

        if request.method == 'POST':
            # Get data from the form
            form = ProfileForm(request.POST)

            # Clean data to avoid injection
            if form.is_valid():
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']

                # Check which data need an update and save in database
                if promo != "":
                    profile.promo = promo
                if campus != "":
                    profile.campus = campus
                profile.save()

        return render(request, 'profil.html', context)

    else:
        return redirect('/')


def home(request):
    if request.user.is_authenticated:

        # Get the current user with the corresponding profile and user's groups
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        groups = Groups.objects.filter(profileID=profile.id)

        # Create list to send data
        lessons = []
        for group in groups:
            lesson = group.lessonID
            if lesson.date >= datetime.date.today():
                lessons.append("Vous avez un cours de {}. Le {} de {} à {}".format(lesson.nom, lesson.date,
                                                                                   lesson.begin, lesson.end))
        # Add the list in context variable
        context = {
            'messages': lessons
        }
        return render(request, 'home.html', context)

    else:
        return redirect('/')


def add(request):
    if request.user.is_authenticated:

        # Get the form from forms.py and add it to the context to send it to the template.
        lessonform = LessonForm()
        context = {
            'lessonform': lessonform
        }
        if request.method == 'POST':
            # Get data from the form
            form = LessonForm(request.POST)

            # Clean data to avoid injection
            if form.is_valid():
                name = form.cleaned_data['name']
                room = form.cleaned_data['room']
                date = form.cleaned_data['date']
                begin = form.cleaned_data['begin']
                end = form.cleaned_data['end']
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']
                subject = form.cleaned_data['subject']

                # Check logic of entries before to save in database
                if date >= datetime.date.today() and begin < end:
                    lesson = Lessons(nom=name, date=date, sujet=subject, promo=promo, begin=begin, campus=campus,
                                     end=end, salle=room)
                    lesson.save()

                    # Get current user and save it as teacher for the lesson
                    user = User.objects.get(username=request.user.username)
                    profile = Profiles.objects.get(user_id=user.id)
                    group = Groups(profileID=profile, lessonID=lesson, teacher=True)
                    group.save()

                    # result is the message to display after the completion of the form good or error
                    context['result'] = "Ce cours a bien été enregistré"
                else:
                    context['result'] = "Veuillez entrer des informations cohérentes"

        return render(request, 'add.html', context)

    else:
        return redirect('/')


def search(request):
    if request.user.is_authenticated:

        # Get the form from forms.py and add it to the context to send it to the template.
        searchform = SearchForm()
        context = {
            'searchform': searchform
        }

        if request.method == 'POST':
            # Get data from the form
            form = SearchForm(request.POST)

            # Clean data to avoid injection
            if form.is_valid():
                name = form.cleaned_data['name']
                date = form.cleaned_data['date']
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']

                # Get every lesson since the current day
                finds = Lessons.objects.filter(date__gte=datetime.date.today())

                # If the date entered is before the current day do the request again
                if date is not None:
                    if date < datetime.date.today():
                        finds = Lessons.objects.filter(date=date)
                    else:
                        finds = finds.filter(date=date)

                # Apply others filter if entered
                if name != "":
                    finds = finds.filter(nom=name)
                if promo != "":
                    finds = finds.filter(promo=promo)
                if campus != "":
                    finds = finds.filter(campus=campus)

                # List of group corresponding only the teacher line to get every informations about profile and lesson
                groups = []
                for lesson in finds:
                    groups.append(Groups.objects.get(lessonID=lesson, teacher=True))
                context['lessons'] = groups

        return render(request, 'search.html', context)

    else:
        return redirect('/')


def subscribe(request, lesson_id):
    if request.user.is_authenticated:

        # Get the current user and the corresponding profile
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)

        # Get the lesson from the id set in url and the corresponding group's entries
        lesson = Lessons.objects.get(id=lesson_id)
        group = Groups.objects.filter(lessonID=lesson)

        # If more than 5 users are already registered the lesson are unavailable
        if len(group) > 5:
            context = {
                'disponible': False
            }
        else:

            # Check if the user is already registered for this lesson
            already = False
            for person in group:
                if person.profileID == profile:
                    already = True
                    context = {
                        'already': True
                    }

            # Finally get success message and save the entry in the database
            if not already:
                context = {
                    'disponible': True
                }
                subscriber = Groups(lessonID=lesson, profileID=profile)
                subscriber.save()

        return render(request, 'subscribe.html', context)

    else:
        return redirect('/')


def view_logout(request):
    logout(request)
    return redirect('/')


def load_search(request):
    finds = Lessons.objects.all()
    data = []
    for lesson in finds:
        x = {
            "title": lesson.nom,
            "description": lesson.sujet,
            "start": lesson.date.strftime("%Y/%m/%d"),
            "end": lesson.date.strftime("%Y/%m/%d"),
            "salle": lesson.salle,
            "id": lesson.id
        }
        data.append(x)
    json_data = json.dumps(data)

    return HttpResponse(json.dumps(data))
