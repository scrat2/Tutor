import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from lesson.forms import ConnexionForm, ProfileForm, LessonForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lesson.models import Profiles, Lessons, Groups


# Other function
def clear_data(data):
    data = data.replace("<", "")
    data = data.replace(">", "")
    return data


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
        lessonform = LessonForm()
        context = {
            'lessonform': lessonform
        }

        # Get all your lesson and sort them
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        all_group = Groups.objects.filter(profileID=profile)
        teacher_lesson = []
        follow_lesson = []
        for group in all_group:
            if group.teacher and group.lessonID.date >= datetime.date.today():
                teacher_lesson.append(group)
            else:
                if group.lessonID.date >= datetime.date.today():
                    follow_lesson.append(Groups.objects.get(lessonID=group.lessonID, teacher=True))

        # Add lesson in the context
        context['teacher_lesson'] = teacher_lesson
        context['follow_lesson'] = follow_lesson

        # Check the form
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                room = form.cleaned_data['room']
                date = form.cleaned_data['date']
                begin = form.cleaned_data['begin']
                end = form.cleaned_data['end']
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']
                subject = form.cleaned_data['subject']

                # clear xss
                name = clear_data(name)
                room = clear_data(room)
                promo = clear_data(promo)
                campus = clear_data(campus)
                subject = clear_data(subject)

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

        return render(request, 'home.html', context)
    else:
        return redirect('/')


def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.POST['id'] is not None:
            idlesson = request.POST['id']

            context = {
                'reponse': 'Echec'
            }

            # Get the current user and the corresponding profile
            user = User.objects.get(username=request.user.username)
            profile = Profiles.objects.get(user_id=user.id)

            # Get the lesson from the id set in url and the corresponding group's entries
            lesson = Lessons.objects.get(id=idlesson)
            group = Groups.objects.filter(lessonID=lesson)

            # If more than 5 users are already registered the lesson are unavailable
            if len(group) > 5:
                context['reponse'] = 'Il y a déjà trop de monde pour ce cours'
            elif lesson.date < datetime.date.today():
                context['reponse'] = 'Ce cours est déjà passé'
            else:
                # Check if the user is already registered for this lesson
                already = False
                for person in group:
                    if person.profileID == profile:
                        already = True
                        context['reponse'] = 'Vous êtes déjà inscrit'

                # Finally get success message and save the entry in the database
                if not already:
                    context['reponse'] = 'Vous êtes inscrit avec succès'
                    subscriber = Groups(lessonID=lesson, profileID=profile)
                    subscriber.save()
            return HttpResponse(json.dumps(context))
        return render(request, 'search.html')
    else:
        return redirect('/')


def load_search(request):
    # Get all data and send it in the list data
    finds = Lessons.objects.all()
    data = []
    for lesson in finds:
        start = lesson.date.strftime("%Y/%m/%d") + ", " + lesson.begin.strftime("%H:%M:%S")
        end = lesson.date.strftime("%Y/%m/%d") + ", " + lesson.end.strftime("%H:%M:%S")
        group = Groups.objects.get(lessonID=lesson, teacher=True)
        nb_participant = Groups.objects.filter(lessonID=lesson).count()
        x = {
            "title": lesson.nom,
            "description": lesson.sujet,
            "start": start,
            "end": end,
            "teacher": group.profileID.user.username,
            "salle": lesson.salle,
            "id": lesson.id,
            "participant": nb_participant - 1
        }
        data.append(x)

    return HttpResponse(json.dumps(data))


def view_logout(request):
    logout(request)
    return redirect('/')
